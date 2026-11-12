#!/bin/bash
# runs the scope probe on every ASGI server and prints the comparison
C=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
D=$(dirname $C)

PY=${PY:-python}
export PYTHONPATH=$C:$D/pylib
cd $C

start() {
    name=$1
    port=$2
    export TRACE=$C/trace-$name.jsonl
    rm -f $TRACE
    case $name in
    netius) cmd="$PY -c \"import os, logging, netius.servers, scope_app; netius.servers.ASGIServer(app=scope_app.app, asyncio=True, poll_timeout=0.002, level=logging.WARNING).serve(host='127.0.0.1', port=$port)\"" ;;
    uvicorn) cmd="$PY -m uvicorn scope_app:app --host 127.0.0.1 --port $port --log-level warning" ;;
    hypercorn) cmd="$PY -m hypercorn scope_app:app --bind 127.0.0.1:$port --log-level warning" ;;
    granian) cmd="$PY -m granian --interface asgi --host 127.0.0.1 --port $port --log-level warning scope_app:app" ;;
    daphne) cmd="$PY -m daphne -b 127.0.0.1 -p $port scope_app:app" ;;
    esac
    eval "nohup $cmd > $C/server-$name.log 2>&1 &"
    echo $! > $C/server-$name.pid
    for index in $(seq 1 30); do
        curl -s -m 1 -o /dev/null 127.0.0.1:$port/ready && break
        sleep 0.5
    done
}

stop() {
    kill $(cat $C/server-$1.pid) 2>/dev/null
    for index in $(seq 1 20); do
        ss -Hltn | grep -q ":$2 " || break
        sleep 0.5
    done
    sleep 1
}

port=18950
for name in netius uvicorn hypercorn granian daphne; do
    port=$((port + 1))
    start $name $port
    # forwarded headers, encoded path and query, repeated headers, gzip
    curl -s -o /dev/null -H "X-Forwarded-Proto: https" -H "X-Forwarded-For: 203.0.113.7" \
        -H "X-Multi: one" -H "X-Multi: two" -H "Accept-Encoding: gzip" \
        "127.0.0.1:$port/probe/caf%C3%A9%20x?q=%C3%A9&a=1&a=2"
    # chunked request body (3 chunks, 30 bytes)
    $PY - $port <<'EOF'
import socket, sys
port = int(sys.argv[1])
sock = socket.create_connection(("127.0.0.1", port))
sock.sendall(b"POST /chunked HTTP/1.1\r\nHost: 127.0.0.1\r\nTransfer-Encoding: chunked\r\nConnection: close\r\n\r\n")
for _index in range(3):
    sock.sendall(b"a\r\n" + b"0123456789" + b"\r\n")
sock.sendall(b"0\r\n\r\n")
response = b""
while True:
    data = sock.recv(65536)
    if not data:
        break
    response += data
print("  chunked response head:", response.split(b"\r\n\r\n")[0].decode("latin-1").replace("\r\n", " | "))
EOF
    # websocket with forwarded headers
    $PY - $port <<'EOF'
import sys, asyncio, websockets
async def main(port):
    async with websockets.connect("ws://127.0.0.1:%s/ws/probe?x=1" % port, additional_headers={"X-Forwarded-Proto": "https"}) as socket:
        await socket.send("hi")
        print("  websocket:", await socket.recv())
asyncio.run(main(sys.argv[1]))
EOF
    stop $name $port
    echo "== $name done ($(grep -c . $C/trace-$name.jsonl) records)"
done
