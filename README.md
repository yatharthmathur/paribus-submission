# Hospital Directory System Backend

A production-ready FastAPI backend scaffold with `uv`-managed dependencies and Docker support.

## Stack

- FastAPI as the HTTP adapter
- Ports-and-adapters (hexagonal) application structure
- SQLAlchemy as a persistence adapter
- SQLite by default, with configurable Postgres / MySQL / MSSQL support
- Uvicorn
- `uv` for dependency management and locking
- Docker + Docker Compose for portable deployment
- Pytest / Ruff / Mypy for quality checks

## Project Structure

```text
.
├── app/
│   ├── adapters/
│   │   └── persistence/
│   │       └── sqlalchemy/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── exception_handlers.py
│   │   └── routes.py
│   ├── application/
│   │   ├── commands.py
│   │   ├── ports.py
│   │   └── services.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── domain/
│   │   ├── exceptions.py
│   │   └── hospital.py
│   ├── schemas/
│   │   └── hospital.py
│   └── main.py
├── tests/
│   ├── test_health.py
│   └── test_hospitals.py
├── .env.example
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── pyproject.toml
└── uv.lock
```

## Local Development with `uv`

1. Install `uv`: https://docs.astral.sh/uv/
2. Create an environment file:

   ```sh
   cp .env.example .env
   ```

3. Sync dependencies:

   ```sh
   uv sync --dev
   ```

4. Run the API:

   ```sh
   uv run python main.py
   ```

   The app will be available at `http://127.0.0.1:8000`.

## Useful Commands

```sh
uv run pytest
uv run ruff check .
uv run ruff format .
uv run mypy app tests
```

## Pre-commit

Install a modern `pre-commit` version (3.7+ recommended), then enable hooks:

```sh
uv tool install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

Run all hooks manually:

```sh
pre-commit run --all-files
pre-commit run pytest --hook-stage manual
```

This project uses isolated pre-commit environments for `mypy` and `pytest`, so hooks run consistently even before you have synced a local `.venv`.

## Architecture

Business logic is isolated from FastAPI and SQLAlchemy using ports and adapters:

- **Domain layer** holds business entities and business exceptions.
- **Application layer** defines ports and use-case services.
- **Adapters** implement those ports, such as SQLAlchemy persistence.
- **API layer** only translates HTTP requests/responses and delegates to application services.

This makes it easier to extend business rules or swap adapters without changing core application logic.

## Database Configuration

The app uses SQLite by default:

```text
sqlite:///./hospital_directory.db
```

You can switch databases by setting `DATABASE_URL` to any SQLAlchemy-compatible connection string and installing the matching driver.

Examples:

```text
# SQLite
sqlite:///./hospital_directory.db

# PostgreSQL
postgresql+psycopg://user:password@localhost:5432/hospital_directory

# MySQL
mysql+pymysql://user:password@localhost:3306/hospital_directory

# Microsoft SQL Server
mssql+pyodbc://user:password@localhost:1433/hospital_directory?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
```

Optional dependency extras are available for driver installation:

```sh
uv sync --extra postgres
uv sync --extra mysql
uv sync --extra mssql
```

Note: MSSQL typically requires system ODBC libraries in addition to the Python package.

## Docker Deployment

Build and run locally with Docker Compose:

```sh
docker compose up --build
```

Run detached:

```sh
docker compose up --build -d
```

The API will be exposed on `http://127.0.0.1:${HOST_PORT:-8000}`.

## Environment Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `APP_NAME` | `Hospital Directory System` | FastAPI application title |
| `APP_VERSION` | `0.1.0` | Version exposed by the API |
| `APP_ENV` | `development` locally / `production` in Compose | Controls reload behavior |
| `APP_HOST` | `0.0.0.0` | Bind host |
| `APP_PORT` | `8000` | Internal application port |
| `PORT` | unset | Platform-provided port override (for Render and similar platforms) |
| `DATABASE_URL` | `sqlite:///./hospital_directory.db` locally | SQLAlchemy connection string |
| `LOG_LEVEL` | `INFO` | Uvicorn log level |
| `HOST_PORT` | `8000` | Host port published by Docker Compose |

## Endpoints

- `GET /` - healthcheck endpoint
- `POST /hospitals` - create a hospital record
- `GET /hospitals` - list hospitals, with optional `active` and `creation_batch_id` filters
- `GET /hospitals/{id}` - fetch a hospital by ID
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
