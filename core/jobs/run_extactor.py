# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core.jobs import job_info_extractor
from rq import Queue
from core import worker
from core import RedisNLP
import json
import ast
from datetime import datetime, timedelta
import datetime
import time

def run_extactor():
    print("""
            Start EXTRACTOR ...
        """)
    q = Queue(connection=worker.W.get_connection())
    key_promed = 'promed'
    redis = RedisNLP(db=1)
    print(redis.get_redis().llen(key_promed))

    for r in range(0,redis.get_redis().llen(key_promed)):
        o = eval(ast.literal_eval(json.dumps(str(
            redis.get_redis().lpop(key_promed).decode('utf-8').replace("'", "||").replace("\"", "'").replace("||","\"")))))
        print(o)
        try:
            job = q.enqueue(job_info_extractor.start_extractor, o['urls'][0], {'data': o['data']},o['content'],timeout=3600)
            print(job.get_id())
        except ValueError:
            print(ValueError)
        time.sleep(1)

    return True

# d = "16-05-2017"
# print(d)
# print(datetime.today().strftime("%d-%m-%Y"))
# print(datetime.strptime(d, "%d-%m-%Y").strftime("%d-%m-%Y") == datetime.today().strftime("%d-%m-%Y"))
# print((datetime.strptime(d, "%d-%m-%Y") - timedelta(days=1)))
# print((datetime.strptime(d, "%d-%m-%Y") - timedelta(days=1)).strftime("%d-%m-%Y"))
#
# d=("﻿15 Apr 2017").strip('\ufeff')
# print(d)
# print(datetime.strptime(d, "%d %b %Y").date().day)
# print(o['data'])
#     print(type(o['data']))
#     print((o['data'] - timedelta(days=1)))
#     print(o['data'].strftime("%d-%m-%Y"))
#     print(datetime.date.today().strftime("%d-%m-%Y"))
#     print(o['data'].strftime("%d-%m-%Y") == datetime.date.today().strftime("%d-%m-%Y"))
#     print(o['data'].strftime("%d-%m-%Y") > datetime.date.today().strftime("%d-%m-%Y"))
#     print(o['data'].strftime("%d-%m-%Y") < datetime.date.today().strftime("%d-%m-%Y"))