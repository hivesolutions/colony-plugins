# Asyncio Runtime Prototype

> **Throwaway prototype, never merge this branch.** It backs the OMN-023 design issue of Omni (asyncio runtime), where the decisions, the measurements and the work items are described.

The branch holds the changes the prototype made to the plugins, all of them still parsed by Python 2:

- `wsgi/src/wsgi/system.py`: `handle` resumes a request whose async action is pending (dispatch half and response half)
- `rest/src/rest/system.py`: the request end notification waits for the pending coroutine
- `mvc/src/mvc/system.py`: the coroutine returned by an `async def` action is kept in the request
- `mvc/src/mvc_utils/system.py`: binds `entity_model_a` (Python 3.7+) next to the sync model functions
- `data/src/entity_manager/structures.py` and `system.py`: lazy loading guard, `system_a` mixin under Python 3.7+

And two new Python 3.7+ modules:

- `data/src/entity_manager/system_a.py`: aiomysql pool per event loop, connection and transaction bound to a context variable, `find_a`, `get_a`, `count_a`, `update_a`, `execute_a`, `transaction_a`, the lazy loading error
- `mvc/src/mvc_utils/entity_model_a.py`: `Model.get_a`, `Model.find_a`, `Model.count_a`, `entity.load_a`, `entity.update_a`

This folder holds the rest:

- `colony_asgi.py`: the ASGI adapter (sibling of `colony_wsgi`) served by the netius ASGI server in asyncio mode
- `plugins/proto_async`: a throwaway Omni plugin with sync and async twins of a few actions and the WebSocket handlers
- `probe_app.py` and `probe_run.sh`: a bare ASGI application probing the netius native and asyncio modes
- `bench.py`: the mixed load generator (fast and slow clients, round robin over ports)
- `ws_check.py`: the WebSocket checks (long task progress and live POS events)
- `results/bench.jsonl`: the raw benchmark results

## Running

```bash
# the async libraries, kept out of the main environment
python -m pip install --target proto/asyncio/pylib aiomysql websockets psutil

# a scratch MariaDB with the Omni demo data
docker run -d --rm --name omni-asyncio-proto-db -e MARIADB_ROOT_PASSWORD=root \
    -e MARIADB_DATABASE=omni_proto -p 127.0.0.1:33071:3306 mariadb:11.4
source proto/asyncio/env.sh
(cd $OMNI && $PY scripts/load_demo_data.py)

# the ASGI runtime (add CHILDREN=4 for pre-fork workers)
PORT=18700 $PY proto/asyncio/colony_asgi.py

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

The complete results (netius modes, isolation, WebSockets, pre-fork workers) are in the OMN-023 issue.
