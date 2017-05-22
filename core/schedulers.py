# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core.jobs import run_extactor
from core.jobs import start_promed
from rq import Queue
from rq.job import Job
import os
import redis
from core import worker
from redis import Redis
from rq_scheduler import Scheduler
from datetime import datetime
from datetime import timedelta
import schedule
import time
import threading

class Schedulers(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.q = Queue(connection=worker.W.get_connection())
        self.ONE_HOUR = 18000

    def run(self):
        print("... Start Schedulers ... ")
        print(os.environ)
        while True:
            print("... SSchedulers ... ")
            job = self.q.enqueue(start_promed,timeout=3600)
            job = self.q.enqueue(run_extactor,timeout=3600)
            time.sleep(self.ONE_HOUR)


if __name__ == "__main__":
    s = Schedulers()
    s.start()

# execute job each 30 minutes for init info extractor function
# job = scheduler.schedule(
#     scheduled_time=datetime.utcnow(),   # Time for first execution, in UTC timezone
#     func=run_extactor,                  # Function to be queued
#     args=[],                            # Arguments passed into function when executed
#     kwargs={},                          # Keyword arguments passed into function when executed
#     # interval=3600,                      # Time before the function is called again, in seconds
#     interval=3,                      # Time before the function is called again, in seconds
#     repeat=None                         # Repeat this number of times (None means repeat forever)
# )
#
# # execute job each 30 minutes for init promed function
# job2 = scheduler.schedule(
#     scheduled_time=datetime.utcnow(),   # Time for first execution, in UTC timezone
#     func=start_promed,                  # Function to be queued
#     args=[],                            # Arguments passed into function when executed
#     kwargs={},                          # Keyword arguments passed into function when executed
#     # interval=3600,                      # Time before the function is called again, in seconds
#     interval=3,                      # Time before the function is called again, in seconds
#     repeat=None                         # Repeat this number of times (None means repeat forever)
# )
#
#
# for s in scheduler.get_jobs():
#     print(s)
#     scheduler.cancel(s)
#
# def count_words_at_url(url):
#     resp = requests.get(url)
#     return len(resp.text.split())
# def get_status(job_key):
#     job = Job.fetch(job_key, connection=conn)
#     if job.is_finished:
#         return 'finalizado'
#     else:
#         return 'ainda processando...'
# def start_job(url):
#     job = q.enqueue(start, url)
#     print(job.get_id())
# def list():
#     print(q.jobs)
# start_job("http://agenciabrasil.ebc.com.br/geral/noticia/2017-05/secretaria-de-saude-de-minas-investiga-11-mortes-com-suspeita-de-chikungunya")
# print(get_status('17d5fcae-c288-4367-9915-8c7482cc6a91'))
# list()
