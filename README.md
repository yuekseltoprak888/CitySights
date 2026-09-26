# EnergyOS

EnergyOS is a Swiss B2B energy assessment platform for commercial and residential properties.

This repository is the project foundation. The assessment workflow is not implemented yet.

```text
Address → building data → roof / solar potential → electricity consumption
→ PV simulation → battery simulation → electricity tariff → financial analysis
→ dashboard → PDF report
```

The product is Switzerland only.

## Local development

Docker Compose runs PostGIS, the API, and the web app.

```bash
docker compose up --build
```

- Web: http://localhost:3000
- API: http://localhost:8000/api/v1/health
- OpenAPI: http://localhost:8000/docs

The API container applies database migrations on startup.

Copy the example environment files when running a service on the host:

```bash
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env
```

Host API commands, from `apps/api`:

```bash
uv sync --group dev
uv run alembic upgrade head
uv run uvicorn energyos.main:app --reload
uv run pytest
uv run ruff check .
uv run mypy
```

Host web commands, from `apps/web`:

```bash
pnpm install
pnpm dev
pnpm test
pnpm lint
pnpm typecheck
```

## Layout

```text
apps/api    FastAPI, SQLAlchemy, Alembic
apps/web    Next.js App Router
docs        Architecture and provider notes
```

Routes stay thin. Business rules live in services. External Swiss datasets will be adapters behind domain ports. Energy calculations and financial calculations stay in separate packages.

## Out of scope

Heat pumps, EV charging, energy trading, IoT, machine learning, portfolio optimization, countries other than Switzerland, and the assessment workflow itself.
