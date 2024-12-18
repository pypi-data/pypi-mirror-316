import sys
import os
import os.path as op
import tempfile
from subprocess import Popen, check_output, PIPE, STDOUT, CalledProcessError
from tiledb.cloud._vendor.cloudpickle.compat import pickle
from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor

import psutil
from tiledb.cloud._vendor.cloudpickle import dumps
from subprocess import TimeoutExpired

loads = pickle.loads
TIMEOUT = 60
TEST_GLOBALS = "a test value"


def make_local_function():
    def g(x):
        # this function checks that the globals are correctly handled and that
        # the builtins are available
        assert TEST_GLOBALS == "a test value"
        return sum(range(10))

    return g


def _make_cwd_env():
    """Helper to prepare environment for the child processes"""
    cloudpickle_repo_folder = op.normpath(
        op.join(op.dirname(__file__), '..'))
    env = os.environ.copy()
    pythonpath = "{src}{sep}tests{pathsep}{src}".format(
        src=cloudpickle_repo_folder, sep=os.sep, pathsep=os.pathsep)
    env['PYTHONPATH'] = pythonpath
    return cloudpickle_repo_folder, env


def subprocess_pickle_string(input_data, protocol=None, timeout=TIMEOUT,
                             add_env=None):
    """Retrieve pickle string of an object generated by a child Python process

    Pickle the input data into a buffer, send it to a subprocess via
    stdin, expect the subprocess to unpickle, re-pickle that data back
    and send it back to the parent process via stdout for final unpickling.

    >>> testutils.subprocess_pickle_string([1, 'a', None], protocol=2)
    b'\x80\x02]q\x00(K\x01X\x01\x00\x00\x00aq\x01Ne.'

    """
    # run then pickle_echo(protocol=protocol) in __main__:

    # Protect stderr from any warning, as we will assume an error will happen
    # if it is not empty. A concrete example is pytest using the imp module,
    # which is deprecated in python 3.8
    cmd = [sys.executable, '-W ignore', __file__, "--protocol", str(protocol)]
    cwd, env = _make_cwd_env()
    if add_env:
        env.update(add_env)
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env,
                 bufsize=4096)
    pickle_string = dumps(input_data, protocol=protocol)
    try:
        comm_kwargs = {}
        comm_kwargs['timeout'] = timeout
        out, err = proc.communicate(pickle_string, **comm_kwargs)
        if proc.returncode != 0 or len(err):
            message = "Subprocess returned %d: " % proc.returncode
            message += err.decode('utf-8')
            raise RuntimeError(message)
        return out
    except TimeoutExpired as e:
        proc.kill()
        out, err = proc.communicate()
        message = "\n".join([out.decode('utf-8'), err.decode('utf-8')])
        raise RuntimeError(message) from e


def subprocess_pickle_echo(input_data, protocol=None, timeout=TIMEOUT,
                           add_env=None):
    """Echo function with a child Python process
    Pickle the input data into a buffer, send it to a subprocess via
    stdin, expect the subprocess to unpickle, re-pickle that data back
    and send it back to the parent process via stdout for final unpickling.
    >>> subprocess_pickle_echo([1, 'a', None])
    [1, 'a', None]
    """
    out = subprocess_pickle_string(input_data,
                                   protocol=protocol,
                                   timeout=timeout,
                                   add_env=add_env)
    return loads(out)


def _read_all_bytes(stream_in, chunk_size=4096):
    all_data = b""
    while True:
        data = stream_in.read(chunk_size)
        all_data += data
        if len(data) < chunk_size:
            break
    return all_data


def pickle_echo(stream_in=None, stream_out=None, protocol=None):
    """Read a pickle from stdin and pickle it back to stdout"""
    if stream_in is None:
        stream_in = sys.stdin
    if stream_out is None:
        stream_out = sys.stdout

    # Force the use of bytes streams under Python 3
    if hasattr(stream_in, 'buffer'):
        stream_in = stream_in.buffer
    if hasattr(stream_out, 'buffer'):
        stream_out = stream_out.buffer

    input_bytes = _read_all_bytes(stream_in)
    stream_in.close()
    obj = loads(input_bytes)
    repickled_bytes = dumps(obj, protocol=protocol)
    stream_out.write(repickled_bytes)
    stream_out.close()


def call_func(payload, protocol):
    """Remote function call that uses cloudpickle to transport everthing"""
    func, args, kwargs = loads(payload)
    try:
        result = func(*args, **kwargs)
    except BaseException as e:
        result = e
    return dumps(result, protocol=protocol)


class _Worker:
    def __init__(self, protocol=None):
        self.protocol = protocol
        self.pool = ProcessPoolExecutor(max_workers=1)
        self.pool.submit(id, 42).result()  # start the worker process

    def run(self, func, *args, **kwargs):
        """Synchronous remote function call"""

        input_payload = dumps((func, args, kwargs), protocol=self.protocol)
        result_payload = self.pool.submit(
            call_func, input_payload, self.protocol).result()
        result = loads(result_payload)

        if isinstance(result, BaseException):
            raise result
        return result

    def memsize(self):
        workers_pids = [p.pid if hasattr(p, "pid") else p
                        for p in list(self.pool._processes)]
        num_workers = len(workers_pids)
        if num_workers == 0:
            return 0
        elif num_workers > 1:
            raise RuntimeError("Unexpected number of workers: %d"
                               % num_workers)
        return psutil.Process(workers_pids[0]).memory_info().rss

    def close(self):
        self.pool.shutdown(wait=True)


@contextmanager
def subprocess_worker(protocol=None):
    worker = _Worker(protocol=protocol)
    yield worker
    worker.close()


def assert_run_python_script(source_code, timeout=TIMEOUT):
    """Utility to help check pickleability of objects defined in __main__

    The script provided in the source code should return 0 and not print
    anything on stderr or stdout.
    """
    fd, source_file = tempfile.mkstemp(suffix='_src_test_cloudpickle.py')
    os.close(fd)
    try:
        with open(source_file, 'wb') as f:
            f.write(source_code.encode('utf-8'))
        cmd = [sys.executable, '-W ignore', source_file]
        cwd, env = _make_cwd_env()
        kwargs = {
            'cwd': cwd,
            'stderr': STDOUT,
            'env': env,
        }
        # If coverage is running, pass the config file to the subprocess
        coverage_rc = os.environ.get("COVERAGE_PROCESS_START")
        if coverage_rc:
            kwargs['env']['COVERAGE_PROCESS_START'] = coverage_rc
        kwargs['timeout'] = timeout
        try:
            try:
                out = check_output(cmd, **kwargs)
            except CalledProcessError as e:
                raise RuntimeError("script errored with output:\n%s"
                                   % e.output.decode('utf-8')) from e
            if out != b"":
                raise AssertionError(out.decode('utf-8'))
        except TimeoutExpired as e:
            raise RuntimeError("script timeout, output so far:\n%s"
                               % e.output.decode('utf-8')) from e
    finally:
        os.unlink(source_file)


if __name__ == '__main__':
    protocol = int(sys.argv[sys.argv.index('--protocol') + 1])
    pickle_echo(protocol=protocol)
