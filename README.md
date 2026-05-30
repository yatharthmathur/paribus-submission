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
├── alembic/
│   └── versions/
├── alembic.ini
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
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "describe change"
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

## Alembic Migrations

Schema changes are managed with Alembic.

Apply all migrations:

```sh
uv run alembic upgrade head
```

Create a new migration after changing SQLAlchemy models:

```sh
uv run alembic revision --autogenerate -m "describe change"
```

Roll back one migration:

```sh
uv run alembic downgrade -1
```

For a new environment or deployment target, run migrations before starting the API.

## Adding New APIs

Because this project uses a ports-and-adapters structure, adding a new API usually means touching a few specific layers rather than putting everything in FastAPI routes.

### Layers to update

#### 1. API layer

Files typically involved:

- `app/api/routes.py`
- `app/schemas/...`

Responsibilities:

- define the HTTP route
- validate request payloads/query params
- shape response DTOs
- call the application service

Keep this layer thin. It should not contain business rules or direct SQLAlchemy queries.

#### 2. Application layer

Files typically involved:

- `app/application/commands.py`
- `app/application/services.py`
- sometimes `app/application/ports.py`

Responsibilities:

- define commands/inputs for use cases
- implement business logic
- coordinate repositories through ports
- raise business-level exceptions

This is the main place to add new business behavior.

#### 3. Domain layer

Files typically involved:

- `app/domain/hospital.py`
- `app/domain/exceptions.py`
- other domain modules as the system grows

Responsibilities:

- domain entities
- business exceptions
- domain rules/value objects

Only update this layer when the business concepts themselves change.

#### 4. Adapter layer

Files typically involved:

- `app/adapters/persistence/sqlalchemy/repositories.py`
- `app/adapters/persistence/sqlalchemy/unit_of_work.py`
- `app/adapters/persistence/sqlalchemy/models.py`

Responsibilities:

- implement persistence ports
- translate between domain objects and SQLAlchemy models
- support new database access patterns required by the application layer

Only update this layer when the use case needs new persistence behavior.

#### 5. Migration layer

Files typically involved:

- `alembic/versions/*.py`

Responsibilities:

- evolve the database schema safely

Only add a migration if the database schema changes.

### Typical scenarios

#### Add a read-only API using existing data

Example: a new `GET` endpoint using fields already stored in the database.

Usually update:

- route
- response schema
- service method
- repository method only if current queries are insufficient

No migration is needed if the schema does not change.

#### Add a state-changing API using existing fields

Example: `PATCH /hospitals/{id}/activate`.

Usually update:

- route
- request schema
- command
- service method
- domain exceptions if needed
- port/repository methods if needed

No migration is needed if the data already exists in the schema.

#### Add a new field

Example: `email`, `city`, or `hospital_type`.

Usually update:

- domain entity
- request/response schema
- command/service logic
- SQLAlchemy model
- repository mapping
- Alembic migration

### Recommended workflow

When adding a new API:

1. define the request/response schema
2. add or update the application command/use case
3. implement the service logic
4. extend the port if new persistence behavior is needed
5. implement the adapter/repository behavior
6. add the FastAPI route
7. add or update tests
8. add an Alembic migration if the schema changed

### Rule of thumb

Ask these questions:

- **Is this just HTTP shape?** Update route and schema.
- **Is there business behavior?** Update service, command, and possibly domain exceptions.
- **Does persistence behavior change?** Update ports and repository adapters.
- **Does the schema change?** Add an Alembic migration.

### Scaling tip

As the project grows, single files like `routes.py`, `commands.py`, and `services.py` may become crowded. A natural next step is to split by feature/use case, for example:

- `app/api/routes/hospitals.py`
- `app/application/commands/create_hospital.py`
- `app/application/services/hospital_service.py`
- `app/schemas/hospitals.py`

That keeps the same architecture while making the codebase easier to extend.

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
- `POST /hospitals` - create a hospital record (the `active` field defaults to `true`, and `creation_batch_id` is generated if omitted)
- `GET /hospitals` - list hospitals, with optional `active` and `creation_batch_id` filters
- `GET /hospitals/{id}` - fetch a hospital by ID
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
