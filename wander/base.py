#!/usr/bin/env python
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pickle

def redis_push(redis, key, objects):
    if not (isinstance(objects, tuple) or isinstance(objects, list)):
        objects = [objects]
    pipe = redis.pipeline()
    for obj in objects:
        serialization = pickle.dumps(obj)
        pipe.rpush(key, serialization)
    pipe.execute()
    print('ok')
    
def redis_pop(redis, key, timeout=1):
    serialization = redis.blpop(key, timeout=timeout)
    if serialization:
        return pickle.loads(serialization[1])

def redis_rpoplpush(redis, r_key, l_key):
    serialization = redis.rpoplpush(r_key, l_key)
    if serialization:
        return pickle.loads(serialization)
