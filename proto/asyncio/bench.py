"""
Mixed load generator of the prototype benchmark: fast clients looping
on a fast endpoint and slow clients looping on a slow one (an external
call of 2 s), with the requests spread round robin over a list of ports
(the netius proxy in front of the LDJ ports does the same).

    python bench.py --ports 18800 --fast 16 --slow 4 --duration 20 \
        --fast-path /omni_proto/products_sync.json \
        --slow-path "/omni_proto/slow_sync.json?ms=2000"
"""

import sys
import json
import time
import asyncio
import argparse
import itertools

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


async def client(ports, path, until, timings, errors):
    while time.time() < until:
        port = next(ports)
        try:
            status, elapsed = await request(port, path)
        except Exception:
            errors.append(path)
            continue
        if not status == 200:
            errors.append(status)
            continue
        timings.append(elapsed)


def percentile(values, ratio):
    if not values:
        return float("nan")
    values = sorted(values)
    return values[min(len(values) - 1, int(len(values) * ratio))]


async def main(args):
    ports = [int(value) for value in args.ports.split(",")]
    ports = itertools.cycle(ports)
    process = psutil.Process(args.pid) if args.pid else None
    rss_before = process.memory_info().rss if process else 0
    until = time.time() + args.duration
    fast, slow, errors = [], [], []
    clients = [
        client(ports, args.fast_path, until, fast, errors)
        for _index in range(args.fast)
    ] + [
        client(ports, args.slow_path, until, slow, errors)
        for _index in range(args.slow)
    ]
    if process:
        process.cpu_percent()
    await asyncio.gather(*clients)
    cpu = process.cpu_percent() if process else 0.0
    rss_after = process.memory_info().rss if process else 0
    threads = process.num_threads() if process else 0
    result = dict(
        label=args.label,
        fast_n=len(fast),
        fast_rps=len(fast) / args.duration,
        fast_p50=percentile(fast, 0.50),
        fast_p95=percentile(fast, 0.95),
        fast_p99=percentile(fast, 0.99),
        fast_max=max(fast) if fast else float("nan"),
        slow_n=len(slow),
        slow_p50=percentile(slow, 0.50),
        slow_max=max(slow) if slow else float("nan"),
        errors=len(errors),
        cpu=cpu,
        rss_before_mb=rss_before / 1048576.0,
        rss_after_mb=rss_after / 1048576.0,
        threads=threads,
    )
    print(json.dumps(result))


parser = argparse.ArgumentParser()
parser.add_argument("--label", default="run")
parser.add_argument("--ports", default="18700")
parser.add_argument("--pid", type=int, default=0)
parser.add_argument("--fast", type=int, default=16)
parser.add_argument("--slow", type=int, default=4)
parser.add_argument("--duration", type=float, default=20.0)
parser.add_argument("--fast-path", default="/omni_proto/products_sync.json")
parser.add_argument("--slow-path", default="/omni_proto/slow_sync.json?ms=2000")
asyncio.run(main(parser.parse_args()))
