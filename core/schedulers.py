# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core.jobs import run_extactor
from core.jobs import start_promed
from rq import Queue
import os
from core import worker
import time
import threading

class Schedulers(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.q = Queue(connection=worker.W.get_connection())
        self.ONE_HOUR = 18000

    def run(self):
        while True:
            print("... Run Scheduler ... ")
            self.q.enqueue(start_promed,timeout=3600)
            self.q.enqueue(run_extactor,timeout=3600)
            time.sleep(self.ONE_HOUR)

if __name__ == "__main__":
    s = Schedulers()
    s.start()