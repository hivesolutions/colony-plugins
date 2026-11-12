#!/bin/bash
# functional checks of a running prototype server: checks.sh <port>
D=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd)
C=$D/conformance
source $D/env.sh
B=127.0.0.1:$1
J=$C/cookies-$1.txt
O=$C/page-$1.out
rm -f $J
echo "== routes"
for u in "omni_proto/fast.json" "omni_proto/slow_sync.json?ms=300" "omni_proto/slow_async.json?ms=300" "omni_proto/products_async.json" "omni_proto/lazy_async.json"; do
    curl -s -m 10 -o $O -w "%{http_code} %{time_total}s " "$B/$u"; echo "$u $(head -c 150 $O)"
done
echo "== pages (sync controllers in the pool)"
curl -s -m 30 -b $J -c $J -o $O -w "%{http_code} %{size_download}B " "$B/adm/signin"; echo "GET /adm/signin"
curl -s -m 30 -b $J -c $J -o $O -w "%{http_code} %{redirect_url} " -X POST -d "username=root&password=Root@12345" "$B/adm/login"; echo "POST /adm/login"
for u in /adm/ /ivm/products /ivm/products/405 /sam/sales /ivm/products.json /api/products/405.json /ivm/resources/libs/uxf/css/ux.css; do
    curl -s -m 30 -b $J -c $J -o $O -w "%{http_code} %{size_download}B " "$B$u"; echo "GET $u"
done
echo "== isolation (naive, then async API, then ORM write)"
curl -s -m 10 "$B/omni_proto/isolation_naive.json?mode=write" > /dev/null & sleep 0.3
curl -s -m 10 "$B/omni_proto/isolation_naive.json?mode=read"; echo "  <- reader (naive)"; wait
curl -s -m 10 "$B/omni_proto/isolation_async.json?mode=write" > /dev/null & sleep 0.3
curl -s -m 10 "$B/omni_proto/isolation_async.json?mode=read"; echo "  <- reader (async)"; wait
curl -s -m 10 "$B/omni_proto/isolation_async.json?mode=write&orm=1" & sleep 0.3
curl -s -m 10 "$B/omni_proto/isolation_async.json?mode=read" > /dev/null; wait; echo "  <- writer (ORM)"
echo "== websockets"
sed "s/^BASE = .*/BASE = \"$B\"/" $D/ws_check.py > $C/ws_check_$1.py
timeout 60 $PY -u $C/ws_check_$1.py | grep -E "progress \+ *(212|1013|20[0-9][0-9])|done|fast requests|pos"
