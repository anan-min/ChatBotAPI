import time
from contextlib import contextmanager

@contextmanager
def timing(description: str):
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.2f} seconds to complete")
