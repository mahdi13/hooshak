import time


class HTimer:
    _start = None
    _end = None

    def start(self):
        self._start = time.time()

    def end(self):
        self._end = time.time()

    def end_and_print(self):
        self.end()
        print(f'It takes: {self._end - self._start}')
