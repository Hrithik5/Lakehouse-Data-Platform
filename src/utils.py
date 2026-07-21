import time


class Timer:
    """
    Simple timer utility for measuring execution time.
    """

    def __init__(self):
        self.start_time = time.perf_counter()

    def elapsed(self):
        """
        Returns elapsed time in seconds.
        """
        return round(
            time.perf_counter() - self.start_time,
            2
        )