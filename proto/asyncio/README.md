# Asyncio Runtime Prototype

> **Throwaway prototype, never merge this branch.** It backs the OMN-023 design issue of Omni, [hivesolutions/omni#451](https://github.com/hivesolutions/omni/issues/451), where the decisions, the measurements and the work items are described.

The branch holds the changes the prototype made to the plugins, all of them still parsed by Python 2:

- `wsgi/src/wsgi/system.py`: `handle` resumes a request whose async action is pending (dispatch half and response half)
- `rest/src/rest/system.py`: the request end notification waits for the pending coroutine
- `mvc/src/mvc/system.py`: the coroutine returned by an `async def` action is kept in the request
- `mvc/src/mvc_utils/system.py`: binds `entity_model_a` (Python 3.7+) next to the sync model functions
- `data/src/entity_manager/structures.py` and `system.py`: lazy loading guard, `system_a` mixin under Python 3.7+

And two new Python 3.7+ modules:

- `data/src/entity_manager/system_a.py`: aiomysql pool per event loop, connection and transaction bound to a context variable, `find_a`, `get_a`, `count_a`, `update_a`, `execute_a`, `transaction_a`, the lazy loading error, `close_a` (pools closed by the server shutdown) and the reset of the inherited connections in the child of a fork (`os.register_at_fork`)
- `mvc/src/mvc_utils/entity_model_a.py`: `Model.get_a`, `Model.find_a`, `Model.count_a`, `entity.load_a`, `entity.update_a`

This folder holds the rest:

- `colony_asgi.py`: the ASGI adapter (sibling of `colony_wsgi`), a plain ASGI application served by netius (asyncio mode), uvicorn, hypercorn or gunicorn with the uvicorn worker, which loads every plugin up front and closes the async pools on shutdown
- `plugins/proto_async`: a throwaway Omni plugin with sync and async twins of a few actions and the WebSocket handlers
- `probe_app.py` and `probe_run.sh`: a bare ASGI application probing the netius native and asyncio modes
- `bench.py`: the mixed load generator (fast and slow clients, round robin over ports)
- `bench_multi.py`: the multi process load generator of the worker runs, with the memory of the server processes
- `ws_check.py` and `ws_multi.py`: the WebSocket checks (long task progress, live POS events, repeated connections)
- `results/bench.jsonl`, `results/servers.jsonl` and `results/workers.jsonl`: the raw results (runtime comparison, ASGI servers, workers)

## Running

```bash
# the async libraries and the ASGI servers, kept out of the main environment
python -m pip install --target proto/asyncio/pylib aiomysql websockets psutil \
    "uvicorn[standard]" hypercorn gunicorn uvicorn-worker

# a scratch MariaDB with the Omni demo data
docker run -d --rm --name omni-asyncio-proto-db -e MARIADB_ROOT_PASSWORD=root \
    -e MARIADB_DATABASE=omni_proto -p 127.0.0.1:33071:3306 mariadb:11.4
# a scratch Redis, the workers share the sessions and the POS events through it
docker run -d --rm --name omni-asyncio-proto-redis -p 127.0.0.1:63791:6379 redis:7.4-alpine
source proto/asyncio/env.sh
(cd $OMNI && $PY scripts/load_demo_data.py)

# the ASGI runtime, SERVER selects the server and CHILDREN its workers
cd proto/asyncio
SERVER=netius PORT=18700 $PY colony_asgi.py
SERVER=uvicorn CHILDREN=4 PORT=18700 $PY colony_asgi.py

# or the server's own command line
$PY -m uvicorn colony_asgi:application --port 18700 --workers 4
$PY -m hypercorn colony_asgi:application --bind 127.0.0.1:18700 --workers 4
$PY -m gunicorn colony_asgi:application -k uvicorn_worker.UvicornWorker \
    --workers 4 --preload --bind 127.0.0.1:18700

# today's runtime for the comparison (one port, and the 64 ports of LDJ)
SERVER=netius PORT=18800 $PY -m colony_wsgi
SERVER=netius BASE_PORT=18900 NUMBER_THREADS=64 $PY -m colony_wsgi
```

The prototype routes live under `/omni_proto/` (`fast`, `slow_sync`, `slow_async`, `products_sync`, `products_async`, `lazy_async`, `isolation_async`, `isolation_naive`, `stock_bump`, all `.json`) and the WebSockets under `/ws/progress` and `/ws/pos`.

```bash
# a concurrent writer (holds an uncommitted change for 1 s) and reader
curl "127.0.0.1:18700/omni_proto/isolation_naive.json?mode=write" & sleep 0.3
curl "127.0.0.1:18700/omni_proto/isolation_naive.json?mode=read"

# fast clients with slow ones in flight
$PY proto/asyncio/bench.py --ports 18700 --fast 16 --slow 32 \
    --slow-path "/omni_proto/slow_async.json?ms=2000"
```

## Results

| 16 fast clients plus   | WSGI, 64 ports (LDJ)            | ASGI, slow call sync (pool of 16) | ASGI, slow call async   |
| ---------------------- | ------------------------------- | --------------------------------- | ----------------------- |
| No slow calls          | 496 req/s, p95 48 ms            | 505 req/s, p95 37 ms              | 505 req/s, p95 37 ms    |
| 4 slow calls of 2 s    | 137 req/s, p95 1.5 s            | 503 req/s, p95 37 ms              | 506 req/s, p95 36 ms    |
| 32 slow calls of 2 s   | 31 req/s, p95 2.0 s             | 6.7 req/s, p50 2.0 s              | 501 req/s, p95 39 ms    |

ASGI servers, same application and scenarios (two rounds each, the uvicorn runs with uvloop and httptools):

| One process, 16 fast clients plus | netius (asyncio mode) | uvicorn     | hypercorn   |
| ---------------------------------- | --------------------- | ----------- | ----------- |
| No slow calls (sync database)      | 491 req/s             | 536 req/s   | 477 req/s   |
| No slow calls (async database)     | 493 req/s             | 536 req/s   | 432 req/s   |
| 32 slow async calls                | 493 req/s             | 531 req/s   | 472 req/s   |
| 500 slow async calls               | 431 req/s, p95 62 ms  | 475 req/s, p95 54 ms | 407 req/s, p95 73 ms |

| 4 workers, 32 fast clients | netius (fork)                 | gunicorn + uvicorn worker (preload, fork) | uvicorn (spawn)               | hypercorn (spawn)             |
| -------------------------- | ----------------------------- | ----------------------------------------- | ----------------------------- | ----------------------------- |
| Sync database              | 1514 req/s, p95 35 ms, 316 MB | 1650 req/s, p95 25 ms, 293 MB             | 1639 req/s, p95 25 ms, 394 MB | 1383 req/s, p95 40 ms, 425 MB |
| Async database             | 1374 req/s, p95 42 ms, 329 MB | 1544 req/s, p95 40 ms, 311 MB             | 1521 req/s, p95 35 ms, 412 MB | 1314 req/s, p95 38 ms, 437 MB |

The memory is the unique memory (USS) of all the server processes.

The complete results (netius modes, isolation, WebSockets, pre-fork workers) are in [hivesolutions/omni#451](https://github.com/hivesolutions/omni/issues/451).
