# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from redis import Redis
from rq import Worker, Queue, Connection
listen = ['default']
import time

class W(object):
    conn=None

    @staticmethod
    def get_connection():
        if W.conn == None:
            redis_url = os.getenv('REDISTOGO_URL', 'http://localhost:6379')
            W.conn = Redis(host='redis', port=6379)
        return W.conn

def clear():
    qfail = Queue(connection=W.get_connection())
    qfail.empty()
    print(qfail.count)


if __name__ == '__main__':
    # clear()
    time.sleep(3)
    with Connection(W.get_connection()):

        print("Starting worker...")

        worker = Worker(list(map(Queue, listen)))
        worker.work()