#!/bin/bash
# starts the Omni ASGI runtime on one server: servers.sh <name> <port> [workers]
# (netius, uvicorn, gunicorn-uvicorn, hypercorn, granian, daphne), every server
# runs with its own proxy header processing off (the application applies them)
D=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd)
source $D/env.sh
NAME=$1
PORT=$2
WORKERS=${3:-0}
EXTRA=""
[ "$WORKERS" -gt 1 ] && EXTRA="--workers $WORKERS"
cd $D
case $NAME in
netius) CMD="env SERVER=netius PORT=$PORT CHILDREN=$WORKERS $PY $D/colony_asgi.py" ;;
uvicorn) CMD="$PY -m uvicorn colony_asgi:application --host 127.0.0.1 --port $PORT --no-proxy-headers --no-access-log --log-level warning $EXTRA" ;;
gunicorn-uvicorn) CMD="$PY -m gunicorn colony_asgi:application -k uvicorn_worker.UvicornWorker --workers ${WORKERS/#0/1} --preload --forwarded-allow-ips= --bind 127.0.0.1:$PORT --log-level warning" ;;
hypercorn) CMD="$PY -m hypercorn colony_asgi:application --bind 127.0.0.1:$PORT --workers ${WORKERS/#0/1} --log-level warning" ;;
granian) CMD="$PY -m granian --interface asgi --host 127.0.0.1 --port $PORT --workers ${WORKERS/#0/1} --log-level warning colony_asgi:application" ;;
daphne) CMD="$PY -m daphne -b 127.0.0.1 -p $PORT colony_asgi:application" ;;
esac
nohup $CMD > $D/conformance/server-$NAME-$PORT.log 2>&1 &
echo $! > $D/conformance/server-$NAME-$PORT.pid
for index in $(seq 1 180); do
    curl -s -m 1 -o /dev/null 127.0.0.1:$PORT/api/ping.json && break
    sleep 1
done
