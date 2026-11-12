#!/bin/bash
# environment of the throwaway asyncio prototype, source it from any directory
# (expects the omni, colony-config and omni-config checkouts next to this one)
export P=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
export ROOT=$(cd $P/../.. && pwd)
export OMNI=${OMNI:-$ROOT/../omni}
export PY=${PY:-python}
export PYTHONPATH=$P/pylib:$P
export RUN_MODE=development
export LEVEL=WARNING
export DB_ENGINE=mysql
export DB_HOST=127.0.0.1
export DB_PORT=33071
export DB_USER=root
export DB_PASSWORD=root
export DB_NAME=omni_proto
export PLUGIN_PATH="$OMNI/*/src;$OMNI/*/*src;$ROOT/*/src;$ROOT/*/*src;$P/plugins/*/src"
export META_PATH="$ROOT/../colony-config/*;$ROOT/../omni-config/*"
export COLONY_PREFIX=/mvc
export ALIAS_PATH=$P/alias.json
export AT_TEST_MODE=1
# workers need shared sessions and the shared broker of the POS events
export SESSION=redis
export REDISTOGO_URL=${REDISTOGO_URL:-redis://127.0.0.1:63791}
export HOST=127.0.0.1
