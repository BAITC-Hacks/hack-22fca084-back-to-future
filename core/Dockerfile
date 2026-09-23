FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --create-home --uid 10001 app

FROM base AS runtime
COPY city_core ./city_core
USER app
CMD ["python", "-m", "city_core", "demo"]

FROM base AS check
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY pyproject.toml ./
COPY city_core ./city_core
COPY tests ./tests
USER app
ENV MYPY_CACHE_DIR=/tmp/mypy RUFF_CACHE_DIR=/tmp/ruff
CMD ["sh", "-c", "ruff check . && ruff format --check . && mypy city_core tests && python -m pytest -p no:cacheprovider"]
