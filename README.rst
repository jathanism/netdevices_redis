######################
Redis Completion Notes
######################

Using redis-completion w/ Trigger NetDevices

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

Cookbook
========

Use mappers to return NetDevice objects::

    from redis_completion import RedisEngine
    from trigger.netdevices import NetDevice
    engine = RedisEngine(prefix='netdevices', db=1)
    results = engine.search_json('core1', mappers=[NetDevice])
    print results[0] # => 'core1-asg.ops.sfdc.net'
