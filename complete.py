# pop.py - Test redis_completion w/ Trigger NetDevices

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

def get_engine(prefix=KEY_PREFIX, db=REDIS_DB):
    """Return RedisEngine completion object"""
    engine = redis_completion.RedisEngine(prefix='netdevices', db=1)
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
