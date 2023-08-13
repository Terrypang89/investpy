import investpy
import time
import logging
import datetime
import threading as th
from time import sleep

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.num = 0
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
        print("done thread " + str(self.num))

    def start(self):
        if not self.is_running:
            self._timer = th.Timer(self.interval, self._run)
            self._timer.name = self.num
            print("thread id=" + self._timer.name)
            self._timer.start()
            self.is_running = True
            self.num = self.num + 1

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def setLogger():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='logs_file',
                    filemode='w')
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def run_main():
    tic = time.perf_counter()
    setLogger()
    data = investpy.economic_calendar(importances=["high", "medium"])
    data.head()
    logging.info(",".join([str(datetime.datetime.now()), data.to_string()]))
    toc = time.perf_counter()
    print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

if __name__ == "__main__":
    print("starting...")
    rt = RepeatedTimer(1, run_main)
    try:
        sleep(109)
    finally:
        rt.stop()