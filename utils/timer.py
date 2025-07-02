import time
from contextlib import contextmanager


class ExecutionTimer:
    def __init__(self):
        self.last_execution_time = 0.0

    @contextmanager
    def __call__(self):
        start_time = time.time()
        try:
            yield
        finally:
            self.last_execution_time = time.time() - start_time

    # For use with 'with' statement
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.last_execution_time = time.time() - self.start_time
