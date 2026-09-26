#!/bin/sh
set -eu
cd /app
if [ ! -x node_modules/.bin/next ]; then
  pnpm install --frozen-lockfile
fi
exec pnpm dev
