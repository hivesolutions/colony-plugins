#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Throwaway prototype of the async (await based) twin of the entity
manager API, imported only under Python 3.7+ (async/await syntax and
context variables), the sync API remains untouched.

The connection (and so the transaction) of an async task is bound to
a context variable instead of the thread identifier, as every task of
the event loop shares the same thread.
"""

import os
import sys
import asyncio
import weakref
import contextvars

POOL_SIZE = 16
""" The maximum number of connections of the async pool """

CONNECTION = contextvars.ContextVar("colony_entity_connection", default=None)
""" The connection of the current task, set while in a transaction """

ASYNC = contextvars.ContextVar("colony_entity_async", default=False)
""" If the current task runs async code (lazy loading is refused) """

POOLS = []
""" The (loop, entity manager, pool) tuples of the open async pools """

INSTANCES = weakref.WeakSet()
""" The entity managers created, reset in the child of a fork """


class LazyLoadError(RuntimeError):
    pass


class RowsCursor(object):
    """
    Minimal cursor over an already fetched result set, so that the
    (sync) result mapping of the entity manager can be reused.
    """

    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.rows[0] if self.rows else None

    def close(self):
        pass


class Transaction(object):

    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.outer = None
        self.pool = None
        self.connection = None
        self.token = None

    async def __aenter__(self):
        self.outer = CONNECTION.get()
        if self.outer:
            return self.outer
        self.pool = await self.entity_manager.get_pool_a()
        self.connection = await self.pool.acquire()
        await self.connection.begin()
        self.token = CONNECTION.set(self.connection)
        return self.connection

    async def __aexit__(self, type, value, traceback):
        if self.outer:
            return False
        try:
            if type:
                await self.connection.rollback()
            else:
                await self.connection.commit()
        finally:
            CONNECTION.reset(self.token)
            self.pool.release(self.connection)
        return False


class EntityManagerAsync(object):

    def enter_async(self):
        return ASYNC.set(True)

    def leave_async(self, token):
        ASYNC.reset(token)

    def is_async_context(self):
        return ASYNC.get()

    def _lazy_guard(self, entity, name):
        if not ASYNC.get():
            return
        raise LazyLoadError(
            "relation '%s' of '%s' is not loaded and lazy loading is not "
            "possible in an async context, use eager loading or "
            "'await entity.load_a(\"%s\")'" % (name, entity.__class__.__name__, name)
        )

    async def get_pool_a(self):
        import aiomysql

        loop = asyncio.get_running_loop()
        pools = self.__dict__.setdefault("_pools_a", {})
        locks = self.__dict__.setdefault("_locks_a", {})
        pool = pools.get(loop, None)
        if pool:
            return pool
        lock = locks.setdefault(loop, asyncio.Lock())
        async with lock:
            pool = pools.get(loop, None)
            if pool:
                return pool
            _connection = self.get_connection()._connection
            pool = await aiomysql.create_pool(
                host=_connection.host,
                port=int(_connection.port),
                user=_connection.user,
                password=_connection.password,
                db=_connection.database,
                minsize=1,
                maxsize=POOL_SIZE,
                autocommit=True,
                charset="utf8mb4",
                init_command="set session transaction isolation level %s"
                % _connection.isolation,
            )
            pools[loop] = pool
            POOLS.append((loop, self, pool))
        return pool

    def transaction_a(self):
        return Transaction(self)

    async def execute_a(self, query):
        if self.engine._escape_slash():
            queries = query if type(query) == list else [query]
            queries = [_query.replace("\\", "\\\\") for _query in queries]
            query = queries if type(query) == list else queries[0]
        connection = CONNECTION.get()
        if connection:
            return await self._execute_a(connection, query)
        pool = await self.get_pool_a()
        async with pool.acquire() as connection:
            return await self._execute_a(connection, query)

    async def _execute_a(self, connection, query):
        queries = query if type(query) == list else [query]
        result = ()
        async with connection.cursor() as cursor:
            for _query in queries:
                await cursor.execute(_query)
                result = await cursor.fetchall()
        return result

    async def find_a(self, entity_class, options={}, **kwargs):
        options = self.normalize_options(options) if options else {}
        self.process_kwargs(options, kwargs)
        query, field_names = self._find_query(entity_class, options)
        rows = await self.execute_a(query)
        return self._find_result(entity_class, field_names, options, RowsCursor(rows))

    async def get_a(self, entity_class, id_value, options=None, **kwargs):
        options = self.normalize_options(options) if options else {}
        self.process_kwargs(options, kwargs)
        table_id = entity_class.get_id()
        filters = list(options.get("filters", []))
        filters.append(
            dict(type="equals", fields=(dict(name=table_id, value=id_value),))
        )
        options["filters"] = filters
        result = await self.find_a(entity_class, options)
        return result[0] if result else None

    async def count_a(self, entity_class, options=None, **kwargs):
        options = self.normalize_options(options) if options else {}
        self.process_kwargs(options, kwargs)
        options["count"] = True
        return await self.find_a(entity_class, options)

    async def update_a(self, entity, immutable=True):
        module = sys.modules[self.__class__.__module__]
        entity.validate_u()
        query = self._update_query(entity, immutable=immutable)
        await self.execute_a(query)
        self.map(entity)
        self.enable(entity)
        entity.data_state = module.UPDATED_STATE_VALUE


async def close_a():
    """
    Closes the async pools of the running loop, to be awaited by the
    shutdown of the server (before the loop itself is closed).
    """

    loop = asyncio.get_running_loop()
    for item in list(POOLS):
        _loop, entity_manager, pool = item
        if not _loop == loop:
            continue
        pool.close()
        await pool.wait_closed()
        entity_manager.__dict__.get("_pools_a", {}).pop(loop, None)
        POOLS.remove(item)


def after_fork():
    """
    Drops, in the child of a fork, the connections inherited from the
    parent (opened while the plugins were loaded), as the socket and the
    TLS session of a connection can not be shared between processes, so
    every worker opens its own connections on demand.
    """

    del POOLS[:]
    for entity_manager in list(INSTANCES):
        entity_manager.__dict__.pop("_pools_a", None)
        entity_manager.__dict__.pop("_locks_a", None)
        connection = entity_manager.__dict__.get("connection", None)
        _connection = getattr(connection, "_connection", None)
        if _connection == None:
            continue
        if hasattr(_connection, "connections_map"):
            _connection.connections_map = {}
        if hasattr(_connection, "transaction_level_map"):
            _connection.transaction_level_map = {}


def extend(cls):
    for name, value in EntityManagerAsync.__dict__.items():
        if name.startswith("__"):
            continue
        setattr(cls, name, value)

    init = cls.__init__

    def __init__(self, *args, **kwargs):
        init(self, *args, **kwargs)
        INSTANCES.add(self)

    cls.__init__ = __init__


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=after_fork)
