"""
Multi process load generator (fast clients only) for the pre-fork
runs, so that the client is never the bottleneck, merging the raw
timings of every process into one set of percentiles.

    python bench_multi.py --port 18750 --processes 4 --clients 8 \
        --path /omni_proto/products_sync.json --label "uvicorn 4 workers"
"""

import sys
import json
import time
import asyncio
import argparse
import multiprocessing

sys.path.insert(0, __file__.rsplit("/", 1)[0] + "/pylib")

import psutil


async def request(port, path, timeout=60.0):
    start = time.time()
    reader, writer = await asyncio.wait_for(
        asyncio.open_connection("127.0.0.1", port), timeout
    )
    try:
        writer.write(
            (
                "GET %s HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n" % path
            ).encode()
        )
        await writer.drain()
        data = await asyncio.wait_for(reader.read(), timeout)
    finally:
        writer.close()
    status = int(data.split(b" ", 2)[1]) if data else 0
    return status, (time.time() - start) * 1000.0


async def clients(port, path, count, until):
    timings, errors = [], []

    async def client():
        while time.time() < until:
            try:
                status, elapsed = await request(port, path)
            except Exception as exception:
                errors.append(exception.__class__.__name__)
                continue
            if status == 200:
                timings.append(elapsed)
            else:
                errors.append(status)

    await asyncio.gather(*[client() for _index in range(count)])
    return timings, errors


def worker(arguments):
    port, path, count, until = arguments
    return asyncio.run(clients(port, path, count, until))


def percentile(values, ratio):
    values = sorted(values)
    return values[min(len(values) - 1, int(len(values) * ratio))] if values else 0.0


def server_processes(port):
    pids = set()
    for connection in psutil.net_connections(kind="tcp"):
        if connection.laddr and connection.laddr.port == port:
            if connection.status == psutil.CONN_LISTEN and connection.pid:
                pids.add(connection.pid)
    processes = []
    for pid in pids:
        process = psutil.Process(pid)
        processes.append(process)
        processes.extend(process.children(recursive=True))
    unique = {process.pid: process for process in processes}
    return list(unique.values())


def main(args):
    until = time.time() + args.duration
    with multiprocessing.Pool(args.processes) as pool:
        results = pool.map(
            worker,
            [(args.port, args.path, args.clients, until)] * args.processes,
        )
    timings = [value for result in results for value in result[0]]
    errors = [value for result in results for value in result[1]]
    memory = []
    root = psutil.Process(args.root_pid) if args.root_pid else None
    tree = (
        [root] + root.children(recursive=True) if root else server_processes(args.port)
    )
    for process in tree:
        try:
            info = process.memory_full_info()
            memory.append((info.rss, info.uss))
        except psutil.Error:
            pass
    print(
        json.dumps(
            dict(
                label=args.label,
                rps=len(timings) / args.duration,
                p50=percentile(timings, 0.50),
                p95=percentile(timings, 0.95),
                p99=percentile(timings, 0.99),
                max=max(timings) if timings else 0.0,
                errors=len(errors),
                error_kinds=sorted(set(str(value) for value in errors)),
                processes=len(memory),
                rss_mb=sum(value[0] for value in memory) / 1048576.0,
                uss_mb=sum(value[1] for value in memory) / 1048576.0,
            )
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="run")
    parser.add_argument("--port", type=int, default=18750)
    parser.add_argument("--processes", type=int, default=4)
    parser.add_argument("--clients", type=int, default=8)
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("--path", default="/omni_proto/products_sync.json")
    parser.add_argument("--root-pid", type=int, default=0)
    main(parser.parse_args())
