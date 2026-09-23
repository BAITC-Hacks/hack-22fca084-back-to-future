# Карта кода

**Обновлена:** 2026-09-23

## core/
| Файл | Отвечает за |
|---|---|
| `city_core/models.py` | frozen dataclasses каталога, выбор мэра, ошибки, состояние города, вклады, дельты и outcome |
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
