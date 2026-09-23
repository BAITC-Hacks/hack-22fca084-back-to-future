FROM python:3.12-slim AS dependencies
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --create-home --uid 10001 app
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM dependencies AS runtime
COPY core/city_core ./city_core
COPY server/app ./app
USER app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

FROM dependencies AS check
COPY server/requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY core/city_core ./city_core
COPY server/app ./app
COPY server/tests ./tests
COPY server/pyproject.toml ./
USER app
ENV MYPY_CACHE_DIR=/tmp/mypy RUFF_CACHE_DIR=/tmp/ruff
CMD ["sh", "-c", "ruff check app tests && ruff format --check app tests && mypy app tests city_core && python -m pytest -p no:cacheprovider"]
