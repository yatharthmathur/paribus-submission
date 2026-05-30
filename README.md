# Hospital Directory System Backend

A production-ready FastAPI backend scaffold with `uv`-managed dependencies and Docker support.

## Stack

- FastAPI
- Uvicorn
- `uv` for dependency management and locking
- Docker + Docker Compose for portable deployment
- Pytest / Ruff / Mypy for quality checks

## Project Structure

```text
.
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   └── main.py
├── tests/
│   └── test_health.py
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
| `LOG_LEVEL` | `INFO` | Uvicorn log level |
| `HOST_PORT` | `8000` | Host port published by Docker Compose |

## Endpoints

- `GET /` - healthcheck endpoint
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
