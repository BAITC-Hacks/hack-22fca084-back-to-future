# Стек

**Обновлён:** 2026-09-23

## Ядро
- Python 3.12, стандартная библиотека: `dataclasses`, `decimal` — `core/pyproject.toml`, `core/city_core/`.
- Runtime без сторонних зависимостей, HTTP, БД и вызовов модели.
- pytest 9.1.1, Ruff 0.16.8, mypy 2.3.1 — `core/requirements-dev.in`.
- Полный зафиксированный набор dev-зависимостей — `core/requirements-dev.txt`.

## Инфраструктура
- Docker Compose `include` — `docker-compose.yml`, `core/compose.yml`.
- Python 3.12 slim, отдельные runtime/check стадии, non-root — `core/Dockerfile`.
- `core` — одноразовый CLI-контейнер без портов и сетевого доступа.

## Проверенные команды
- `make up` — сборка и запуск CLI-контейнера.
- `docker compose logs core` — вывод результата; после расчёта контейнер завершается.

- `make core-check` — Ruff, форматирование, mypy, pytest (68 тестов).
- `docker compose run --rm -T core python -m city_core baseline` — точный базовый Score.
- `docker compose run --rm -T core python -m city_core demo` — пример из кейса за 95.
- `docker compose run --rm -T core python -m city_core evaluate < core/tests/fixtures/over_budget.json` — ожидаемый отказ с exit 2.

## API и AI
- FastAPI 0.141.1, Pydantic 2.13.5, Uvicorn 0.53.0, HTTPX 0.28.1 — server/requirements.in, полный lock requirements.txt.
- pydantic-settings — server/requirements.in.
- OpenAI Chat Completions со structured outputs, модель из OPENAI_MODEL (пример gpt-4.1-mini). Без ключа возвращается unavailable.
- Проверено: make api-check (22 теста, Ruff, mypy), make up, GET /api/health, /api/catalog, POST evaluate/analyze на localhost:8020.
- Живые AI-ответы не проверены: пользователь ещё добавляет ключ.
