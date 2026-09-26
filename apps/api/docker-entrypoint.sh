#!/bin/sh
set -eu
cd /app
uv run alembic upgrade head
exec uv run uvicorn energyos.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/src
