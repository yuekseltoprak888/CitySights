# EnergyOS agent guide

EnergyOS is a Swiss B2B assessment platform for commercial and residential properties. The intended workflow is address, building, roof and solar potential, electricity consumption, PV simulation, battery simulation, electricity tariff, financial analysis, dashboard, and PDF report.

That workflow is not in this milestone. Do not add it unless the task asks for a specific step.

## Do not add

Heat pumps, EV charging, energy trading, IoT, machine learning, portfolio optimization, or countries other than Switzerland.

## Run and test

Docker Compose is the full local stack:

```bash
docker compose up --build
```

API, from `apps/api`:

```bash
uv sync --group dev
uv run alembic upgrade head
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Web, from `apps/web`:

```bash
pnpm install
pnpm test
pnpm lint
pnpm typecheck
```

Integration tests need PostGIS. They skip when PostgreSQL is unreachable. CI sets `REQUIRE_DATABASE=1`, so a missing database fails the job.

Copy `apps/api/.env.example` to `apps/api/.env` for host runs. Never commit `.env`. Production rejects the example database password.

## Where code goes

| Change | Location |
| --- | --- |
| HTTP parsing and status codes | `apps/api/src/energyos/api` |
| Use cases | `apps/api/src/energyos/services` |
| Values, units, ports | `apps/api/src/energyos/domain` |
| SQLAlchemy and Alembic | `apps/api/src/energyos/db` and `apps/api/alembic` |
| Swiss or mock datasets | `apps/api/src/energyos/integrations` |
| Wiring | `apps/api/src/energyos/composition.py` |
| Screens | `apps/web/src/features/<step>` |

A route validates input, resolves the organization, calls one service, and maps the result. A new Swiss dataset is a new adapter, not a change to a service.

## Rules that keep the model replaceable

- Domain code does not import FastAPI, SQLAlchemy, HTTP clients, or calculation libraries.
- Energy calculations and financial calculations live in separate packages.
- Services depend on ports. `composition.py` selects the mock adapter until a real provider is registered.
- Quantities carry units. Results carry assumptions and an engine version.
- Prices, tariffs, subsidies, and engineering assumptions are data, not constants.
- Assessment queries are scoped by organization id.
- Logs may include request id and organization id. They omit request bodies, addresses, and provider payloads.
- Store later geometry as SRID 2056. Accept WGS84 at the API edge.
- The web app calls EnergyOS only.

Read `docs/architecture.md`, `docs/api-conventions.md`, `docs/swiss-providers.md`, and `docs/calculations.md` before changing those areas.

## Done

A change is done when it is typed, linted, and tested, and when a new port or table is described in `docs/`.
