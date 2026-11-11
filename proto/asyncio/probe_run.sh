#!/bin/bash
# usage: probe_run.sh <port> [ASYNCIO=0|1] (POLL=<seconds> for the poll timeout)
P=$(dirname $(readlink -f $0))
PY=${PY:-python}
cd $P
PYTHONPATH=$P/pylib:$P PORT=$1 HOST=127.0.0.1 ASYNCIO=${2:-0} LEVEL=WARNING \
    exec $PY -c "
import os, logging, netius.servers
import probe_app
server = netius.servers.ASGIServer(app=probe_app.app, level=logging.WARNING, poll_timeout=float(os.environ.get('POLL', '0.25')))
server.serve(host='127.0.0.1', port=int(os.environ['PORT']), env=True)
"
