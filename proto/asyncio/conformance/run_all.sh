#!/bin/bash
# runs the Omni conformance on every ASGI server, single and 4 workers
D=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd)
C=$D/conformance
OUT=$C/results.txt
: > $OUT
port=18960
for config in "netius 0" "uvicorn 0" "gunicorn-uvicorn 1" "hypercorn 0" "granian 0" "daphne 0" \
    "netius 4" "uvicorn 4" "gunicorn-uvicorn 4" "hypercorn 4" "granian 4"; do
    set -- $config
    port=$((port + 1))
    $C/servers.sh $1 $port $2 > /dev/null
    sleep 3
    result=$($C/omni_conformance.sh $port 2>&1 | tail -1)
    kill $(cat $C/server-$1-$port.pid) 2>/dev/null
    for index in $(seq 1 30); do
        ss -Hltn | grep -q ":$port " || break
        sleep 1
    done
    sleep 2
    echo "$1 workers=$2 | $result | tracebacks=$(grep -c Traceback $C/server-$1-$port.log)" >> $OUT
done
echo done >> $OUT
