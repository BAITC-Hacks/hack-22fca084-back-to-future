# Стек

Обновлён: 2026-09-23. Общая сборка main.

## Клиент

React 19.3.0, TypeScript 6.0.3, Vite 8.3.0, MapLibre GL JS 6.11.1,
CSS Modules, ESLint — `client/package.json`, `client/src/`.
OpenFreeMap/OpenStreetMap — `features/map/mapConfig.ts`.
Versioned localStorage — `features/simulator/storage.ts`.

## API и ядро

Python 3.12; FastAPI 0.141.1, Pydantic 2.13.5, Uvicorn 0.53.0,
HTTPX 0.28.1, pydantic-settings 2.15.0 — `server/requirements.txt`.
Ядро: Decimal и frozen dataclasses, без runtime-зависимостей — `core/city_core/`.
OpenAI Chat Completions: gpt-6-sol, Flex, structured outputs,
reasoning_effort low, timeout180s — `server/app/agent/provider.py`, `config.py`.
БД и регистрации нет.

## Инфраструктура

Docker Compose include; Node22/Nginx1.29Alpine и Python3.12slim.
Источники: `client/Dockerfile`, `server/Dockerfile`, `core/Dockerfile`,
`docker-compose.yml`, `server/compose.yml`, `core/compose.yml`.
Клиент проксирует /api к api:8000; ключ доступен только API.

## Команды

- `make up` — весь стек из одного клона.
- `make ps`, `make logs`, `make down` — управление стеком.
- `make core-check` — Ruff, mypy, 68 pytest тестов.
- `make api-check` — Ruff, mypy, 22 pytest теста.
- `make core-demo`, `make core-baseline` — CLI ядра.
- `npm --prefix client run typecheck`, `npm --prefix client run lint`, `npm --prefix client run test` — проверки клиента после npm ci.

Живой ответ gpt-6-sol Flex проверен через API и браузер.
Полный золотой прогон не выполнен, автоматического runner нет;
кейсы — `server/evals/cases.json`.
