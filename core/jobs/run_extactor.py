# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core.jobs import job_info_extractor
from rq import Queue
from core import RedisNLP
import json
import ast
from datetime import datetime, timedelta
import datetime
import time

def run_extactor():
    q = Queue(connection=RedisNLP.conn(db_=0))
    key_promed = 'promed'
    redis = RedisNLP(db=1)
    for r in range(0,redis.get_redis().llen(key_promed)):
        o = eval(ast.literal_eval(json.dumps(str(
            redis.get_redis().lpop(key_promed).decode('utf-8').replace("'", "||").replace("\"", "'").replace("||","\"")))))
        try:
            job = q.enqueue(job_info_extractor.start_extractor, o['urls'][0], {'data': o['data']},o['content'],timeout=3600)
            print("Enqueue extractor: ",o['data'],o['urls'][0],job.get_id())
        except ValueError:
            print(ValueError)
    return True

# run_extactor()
