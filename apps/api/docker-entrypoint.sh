#!/bin/sh
set -eu
cd /app
uv run --no-sync alembic upgrade head
exec uv run --no-sync uvicorn energyos.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/src
