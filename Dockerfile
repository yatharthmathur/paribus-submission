ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

RUN pip install --no-cache-dir "uv==0.7.22"

COPY pyproject.toml uv.lock README.md ./
RUN mkdir -p app tests
RUN uv sync --frozen --no-dev --no-install-project

COPY app ./app
COPY main.py ./
RUN uv sync --frozen --no-dev

FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    DATABASE_URL=sqlite:////app/data/hospital_directory.db \
    LOG_LEVEL=INFO \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app
COPY --from=builder /app/main.py /app/main.py
COPY pyproject.toml README.md ./

RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD python -c "import os, urllib.request; port = os.getenv('PORT') or os.getenv('APP_PORT') or '8000'; urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=3)"

USER appuser

CMD ["python", "main.py"]
