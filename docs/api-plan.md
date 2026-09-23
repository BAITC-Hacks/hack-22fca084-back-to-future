# План контейнерного API каталога и расчёта

**Статус:** в работе

Цель — поднять воспроизводимый FastAPI-сервис поверх опубликованного `city_core`: healthcheck, каталог с baseline и оценка сценария. Сервер остаётся stateless, не копирует данные/формулу ядра и пока не содержит OpenAI endpoint.

## Контракты шага

- `GET /api/health -> 200 {"status":"ok"}`.
- `GET /api/catalog -> 200 {"catalog": ..., "baseline": ...}`.
- `POST /api/scenarios/evaluate` принимает `selections`; валидный outcome даёт 200, business-invalid outcome — 422 с domain `issues` и `result=null`.
- Malformed JSON/Pydantic input даёт стандартизованный request-validation 422 с location, отдельно от domain issues.
- Decimal из ядра остаются JSON-строками.
- `POST /api/scenarios/analyze` отсутствует до агентного шага.

## Чекбокс-план

- [x] Создать `server/pyproject.toml`, pinned `server/requirements.txt`, `server/Dockerfile`, `server/compose.yml`, пакет `server/app/`; собирать образ из корня с `COPY core`/установкой `city_core`, слушать 8000 и публиковать `127.0.0.1:${API_PORT}`.
- [x] Первым реализовать `server/app/main.py` и `api/health.py`; подключить Docker healthcheck и добиться healthy-состояния через общий Compose до business endpoints.
- [x] В `server/app/schemas/` описать selection/request/issue/outcome/catalog/health модели и сериализацию Decimal строками.
- [x] В `server/app/core_adapter.py` и `api/catalog.py` собрать `{catalog,baseline}` только из `get_catalog()` и `baseline()`, без серверной копии данных.
- [x] В `api/scenarios.py` делегировать `evaluate_scenario()`; вернуть 200 для результата и domain 422 с `issues/result=null` для нарушений правил.
- [x] В `errors.py`, `logging.py`, `server/tests/` стандартизовать malformed 422 и безопасный 500, добавить JSON-логи и HTTPX-тесты health/catalog/evaluate, Decimal, примеров 52.55768/56.54307 и отсутствующего analyze.
- [x] Автоматические проверки: внутри образа пройти Ruff, mypy, pytest; на поднятом контейнере проверить health, OpenAPI, catalog/baseline, valid/domain-invalid/malformed evaluate и bind только на loopback.
- [ ] Ручная проверка: через `/docs` вызвать три endpoint, глазами сверить ответы с контрактом ядра и подтвердить готовность для UI без CORS, БД, auth и analyze.

## Передача и границы

- Шаг ждёт публикации `doszhan`, шаг 1, затем разблокирует `mansur`, шаг 2.
- Nginx same-origin proxy и хранение сценариев принадлежат клиенту.
- OpenAI-анализ, provider timeout и золотой набор не входят в этот план.

## Ускоренный этап AI
По просьбе пользователя до дедлайна добавлены /api/scenarios/analyze, OpenAI structured output, таймаут 30 секунд, максимум два одновременных запроса, явный unavailable без ключа. Перед промптом создан server/evals/cases.json (5 кейсов, 2 негативных). Ключа пока нет: живое поведение модели и золотой набор не проверены. Автотесты API: 22 passed; Ruff/mypy зелёные; проверены реальные HTTP. Ручная приёмка через итоговый клиент впереди.
