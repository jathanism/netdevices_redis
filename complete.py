#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
complete.py - Test redis_completion w/ Trigger NetDevices
"""

from collections import deque
import json
import os
import redis_completion
try:
    from trigger.netdevices.loader import BaseLoader
except ImportError:
    BaseLoader = None

KEY_PREFIX = 'netdevices'
REDIS_DB = 1
NETDEVICES = os.path.join(os.environ['HOME'], 'sandbox/netdevices.json')

def get_data(path=NETDEVICES):
    with open(path) as f:
        return json.load(f)

def get_engine(prefix=KEY_PREFIX, db=REDIS_DB, engine_class=None):
    """Return RedisEngine completion object"""
    if engine_class is None:
        engine_class = redis_completion.RedisEngine
    engine = engine_class(prefix='netdevices', db=1)
    return engine

def populate_netdevices(netdevices, engine):
    """Populate redis_completion with NetDevice JSON objects."""
    results = deque()
    for devobj in netdevices:
        id, _, name = devobj['Name'].split(' / ')
        title = devobj.get('nodeName', name)
        status = engine.store_json(id, title, devobj)
        results.append(status)

    # True if all store_json() calls returned None
    return set(results) == {None}

def filter_dev(**kwargs):
    field, value = kwargs.items()[0]
    return lambda obj: getattr(obj, field, None) == value

class MyRedisEngine(redis_completion.RedisEngine):
    def clean_phrase(self, phrase):
        print 'before:', phrase
        cleaned = super(MyRedisEngine, self).clean_phrase(phrase)
        print ' after:', cleaned
        return cleaned

class RedisLoader(BaseLoader):
    """Load NetDevices from Redis using redis-completion."""
    is_usable = bool(BaseLoader)
    
    def get_data(self, data_source, key_prefix='netdevices'):
        pass

    def load_data_source(self, data_source, **kwargs):
        key_prefix = kwargs.get('key_prefix', 'netdevices')
        try:
            return self.get_data(data_source, key_prefix)
        except Exception as err:
            raise LoaderFailed("Tried %r; and failed: %r" % (data_source, err))

if __name__ == '__main__':
    engine = get_engine()
    netdevices = get_data()
    from trigger.netdevices import NetDevice
    mappers = [NetDevice]
    print engine.search_json('core1', mappers=mappers)

