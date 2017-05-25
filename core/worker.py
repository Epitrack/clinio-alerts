# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from redis import Redis
from rq import Worker, Queue, Connection
listen = ['default']
import time
from core import RedisNLP

def clear():
    qfail = Queue(connection=RedisNLP.conn(db_=0))
    qfail.empty()
    print(qfail.count)

if __name__ == '__main__':
    with Connection(RedisNLP.conn(db_=0)):
        print("Starting worker...")
        worker = Worker(list(map(Queue, listen)))
        worker.work()