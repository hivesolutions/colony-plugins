#!/bin/bash
# server neutral conformance of the Omni ASGI runtime against a running
# server: omni_conformance.sh <port>, prints one summary line
D=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd)
C=$D/conformance

B=127.0.0.1:$1
J=$C/cookies-$1.txt
rm -f $J

# functional checks (routes, pages, isolation, websockets)
out=$($C/checks.sh $1 2>&1)
errors=$(echo "$out" | grep -cE '^[45][0-9][0-9] |^\[[45]')
pages=$(echo "$out" | grep -cE '^200 .*GET /(ivm/products|ivm/products/405|sam/sales|adm/)$')
isolation=$(echo "$out" | grep -c 'ThinkBook Pro 15.*reader (async)')
orm=$(echo "$out" | grep -c '"error":null.*writer')
ws=$(( $(echo "$out" | grep -c 'done') + $(echo "$out" | grep -c '"stock"') ))

# compression (application level, same bytes on every server)
curl -s -b $J -c $J -o /dev/null -X POST -d "username=root&password=Root@12345" "$B/adm/login"
curl -s -b $J -o $C/plain-$1.json "$B/ivm/products.json"
curl -s -b $J -H "Accept-Encoding: gzip" -D $C/gzip-$1.headers -o $C/gzip-$1.bin "$B/ivm/products.json"
encodings=$(grep -ci "^content-encoding: gzip" $C/gzip-$1.headers)
same=$(gunzip -c $C/gzip-$1.bin 2>/dev/null | cmp -s - $C/plain-$1.json && echo yes || echo no)
ratio=$(echo "$(stat -c %s $C/gzip-$1.bin) $(stat -c %s $C/plain-$1.json)" | awk '{printf "%.0f%%", 100 * $1 / $2}')
plain_encoding=$(curl -s -b $J -D - -o /dev/null "$B/ivm/products.json" | grep -ci "^content-encoding")

# forwarded headers (scheme from X-Forwarded-Proto, peer address kept)
direct=$(curl -s "$B/omni_proto/request_info.json")
forwarded=$(curl -s -H "X-Forwarded-Proto: https" -H "X-Forwarded-For: 203.0.113.7" "$B/omni_proto/request_info.json")
location=$(curl -s -D - -o /dev/null -H "X-Forwarded-Proto: https" -X POST -d "username=root&password=Root@12345" "$B/adm/login" | grep -i "^location" | tr -d "\r" | cut -d" " -f2)

echo "errors=$errors pages=$pages/4 isolation=$isolation orm=$orm ws=$ws/3 | gzip: encoded=$encodings identical=$same size=$ratio plain_encoded=$plain_encoding | direct=$(echo $direct | tr -d '{}"' | cut -d, -f1-3) | forwarded=$(echo $forwarded | tr -d '{}"' | cut -d, -f1-3) | login_location=$location"
