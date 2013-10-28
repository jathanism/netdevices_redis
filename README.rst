######################
Redis Completion Notes
######################

Using redis-completion w/ Trigger NetDevices

**This depends on the redis_completion branch of Trigger @ github.com/jathanism/trigger**

URL
    http://redis-completion.readthedocs.org

Dependencies
    redis-py, A Redis server

Stuff to know
=============

prefix
    Prefix to use for the namespace (e.g. 'netdevices')

flush()
    Flush the database

search_json()
    Search and return JSON objects

stop_words
    Words to remove from index/search data

clean_phrase()
    Overload this to customize what gets filtered out of search terms

Cookbook
========

Use mappers to return NetDevice objects::

    from redis_completion import RedisEngine
    from trigger.netdevices import NetDevice
    engine = RedisEngine(prefix='netdevices', db=1)
    results = engine.search_json('core1', mappers=[NetDevice])
    print results[0] # => 'core1-asg.ops.sfdc.net'

Use filters to filter the results::

    def filter_dev(field, value):
        return lambda obj: getattr(obj, field, None) == value
    engine.search_json('core1', mappers=[NetDevice], filters=[filter_dev(vendor='force10'))
