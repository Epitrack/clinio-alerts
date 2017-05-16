from core.jobs import start_extractor
from rq import Queue
from core import worker
from core import RedisNLP
import json
import ast
import datetime

def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)
    return d

def run():
    q = Queue(connection=worker.conn)
    key_promed = 'promed'
    redis = RedisNLP(db=1)

    for r in range(0,redis.get_redis().llen(key_promed)):
        o = redis.get_redis().lpop(key_promed)
        o = json.dumps(str(o.decode('utf-8').replace("'","||").replace("\"","'").replace("||","\"")))
        print(o)
        o = eval(ast.literal_eval(o))
        print(o['link'])
        job = q.enqueue(start_extractor, o['link'])
        print(job.get_id())

    return