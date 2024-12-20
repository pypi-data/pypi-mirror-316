import time
from time import perf_counter

class stopwatch:
    def __enter__(self, action_str: str = None):
        self.action_str = action_str
        self.start = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        elapsed = perf_counter() - self.start

        readout = 'time elapsed was {:.5f}!'.format(elapsed)
        print(readout)

if __name__ == '__main__':
    with stopwatch():
        time.sleep(1)