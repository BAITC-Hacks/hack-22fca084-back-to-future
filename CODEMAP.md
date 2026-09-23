# Карта кода

**Обновлена:** 2026-09-23

## core/
| Файл | Отвечает за |
|---|---|
| `city_core/models.py` | frozen dataclasses каталога, выбор мер, ошибки, состояние города, вклады, дельты и outcome |
| `city_core/catalog.py` | единственный неизменяемый синтетический датасет пяти районов и десяти показателей, а также 14 мер, весов, лагов, синергий и конфликтов |
| `city_core/validation.py` | все ограничения сценария и возврат всех причин нарушений без расчёта score |
| `city_core/calculator.py` | baseline и evaluate_scenario: изолированный Decimal-контекст, сумма эффектов, лаги, синергии, clip, districtScore, cityScore, сравнение до/после и вклады |
| `city_core/serialization.py` | JSON-сериализация Decimal точной строкой и строгий разбор входа selections |
| `city_core/cli.py` | команды catalog, baseline, demo и evaluate, JSON из stdin и exit 2 при ошибке |
| `city_core/__main__.py` | точка входа для запуска через `python -m` |
| `city_core/__init__.py` | публичные импорты без зависимости от HTTP-слоя |
| `tests/` | тесты датасета, правил, формулы, порогов, CLI/JSON и контрольных сценариев 95/61/перерасход |
| `Dockerfile` | стадии runtime/check, Python 3.12 и запуск от non-root без runtime-зависимостей |
| `compose.yml` | одноразовый CLI-контейнер core без сети и портов; профиль check для ruff, mypy и pytest |

## ./
| Файл | Отвечает за |
|---|---|
| `docker-compose.yml` | подключение конфигурации контейнера core |
| `Makefile` | команды запуска стека, проверки core и демонстрационных режимов: up, core-check, core-demo, core-baseline |

## server/
| Файл | Ответственность |
|---|---|
| app/main.py | FastAPI, lifespan HTTPX, лимит одновременных AI-вызовов |
| app/config.py | настройки OpenAI из окружения, секретный тип ключа |
| app/schemas.py | строгий HTTP-вход, типизированный выход ядра |
| app/core_adapter.py | преобразование входа и делегирование расчёта ядру |
| app/api/health.py | независимый healthcheck |
| app/api/catalog.py | каталог и baseline |
| app/api/scenarios.py | evaluate, доменные 422 |
| app/api/analysis.py | проверка сценария, AI-анализ, unavailable/error |
| app/agent/provider.py | OpenAI structured outputs, валидация текста, отказ без утечки ошибки |
| app/agent/prompt.md | качественное объяснение только по вычисленным фактам |
| app/errors.py | безопасная форма ошибок запроса |
| app/logging.py | JSON-логи и request id, обработка 500 |
| tests/ | 22 контрактные проверки HTTP |
| evals/cases.json | пять критериев для будущей проверки живого AI |
| Dockerfile | runtime/check API и импорт ядра |
| compose.yml | API, healthcheck, локальный порт, переменные OpenAI |
