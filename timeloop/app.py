import sys
import signal
import time

from timeloop.exceptions import ServiceExit
from timeloop.job import Job
from timeloop.helpers import service_shutdown


class Timeloop():
    def __init__(self):
        self.job = None
        self.block = False

    def _add_job(self, func, interval, *args, **kwargs):
        j = Job(interval, func, *args, **kwargs)
        self.job = j

    def _block_main_thread(self):
        signal.signal(signal.SIGTERM, service_shutdown)
        signal.signal(signal.SIGINT, service_shutdown)

        while True:
            try:
                time.sleep(1)
            except ServiceExit:
                self.stop()
                break

    def _start_jobs(self, block):
        self.job.daemon = not block
        self.job.start()

    def _stop_jobs(self):
        self.job.stop()

    def add_job(self, interval):
        def decorator(f):
            self._add_job(f, interval)
            return f
        return decorator

    def stop(self):
        self._stop_jobs()

    def start(self, block=False):
        self._start_jobs(block=block)
        if block:
            self.block = True
            self._block_main_thread()

    def restart(self):
        self.job.stop()
        self._add_job(self.job.execute, self.job.interval)
        self.start(self.block)

