import os
ND_PATH = os.path.join(os.environ['HOME'], 'sandbox/netdevices.json')
os.environ['NETDEVICES_SOURCE'] = ND_PATH

import json
import complete
from trigger.netdevices import NetDevice, NetDevices
#from trigger.conf import settings
#nd = NetDevices()
import collections

class RedisNetDevices(NetDevices._actual, collections.MutableMapping):
    class _actual(object):
        # Neutered _Singleton-holding inner class
        pass

    def __init__(self, production_only=True, with_acls=None):
        #super(RedisNetDevices, self).__init__(production_only, with_acls)
        self.engine = complete.get_engine()
        self.client = self.engine.client
        self.id_list = self.client.hkeys(self.engine.data_key)
        self.__mappers = [NetDevice]
        self._keys = None
        self._values = None
        #self.id_list = self._titles.values()

    def keys(self):
        if not self._keys:
            self._keys = self.client.hvals(self.engine.title_key)
        return self._keys

    def values(self):
        if not self._values:
            self._values = self.engine._process_ids(self.id_list, limit=None,
                    filters=None, mappers=[json.loads, NetDevice])
        return list(iter(self))

    @property
    def _mappers(self):
        # Return a copy of self.__mappers
        return self.__mappers[:]

    def _search(self, *args, **kwargs):
        mymappers = self._mappers
        return self.engine.search_json(mappers=mymappers, *args, **kwargs)

    def filter_dev(self, field, value):
        return lambda obj: getattr(obj, field, None) == value

    # Broken... Needs to be optimized to use the new method.
    #def search(self, token, field='nodeName'):
    #    return self._search(token, filters=[self.filter_dev(field, token)])
    #def search(self, *args, **kwargs):
    #    return self.search(*args, **kwargs)
    search = _search

    def __getitem__(self, item):
        try:
            #result = self._search(item, limit=1)[0]
            result = self._search(item)
            if len(result) == 1:
                return self._search(item, limit=1)[0]
            raise IndexError
        except IndexError as err:
            raise KeyError(item)

    def __contains__(self, item):
        try:
            test = self[item]
        except KeyError:
            return False
        else:
            return True
        #test = self.engine.search(item, limit=1) # Don't need JSON; faster
        #return len(test) > 0

    def __len__(self):
        return self.client.hlen(self.engine.data_key)

    def __iter__(self):
        if not self._values:
            values = self.engine._process_ids(self.id_list, limit=None,
                                              filters=None,
                                              mappers=[json.loads, NetDevice])
            self._values = values
        return iter(self._values)

    def __delitem__(self):
        pass

    def __setitem__(self):
        pass

if __name__ == '__main__':
    nd = RedisNetDevices()
