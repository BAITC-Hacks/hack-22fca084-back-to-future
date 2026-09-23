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

## client/
| Файл | Отвечает за |
|---|---|
| `index.html` | русская HTML-точка входа клиентского приложения |
| `tsconfig.json` | строгие настройки TypeScript |
| `vite.config.ts` | сборка React-приложения через Vite |
| `eslint.config.js` | линтинг TypeScript и React hooks |
| `Dockerfile` | сборка Node 22 и runtime на Nginx 1.29 от non-root пользователя |
| `src/main.tsx` | запуск приложения с ленивой загрузкой `MapPage`, `StrictMode` и `ErrorBoundary` |
| `src/features/map/mapConfig.ts` | четыре ориентира Астаны, начальная камера и URL OpenFreeMap |
| `src/features/map/mapStyle.ts` | светлая карта, русские подписи и слои `fill-extrusion` |
| `src/features/map/useCityMap.ts` | жизненный цикл карты и worker, retry и ошибки, камера, режимы 2D/3D, подписи и маркеры |
| `src/shared/api/types.ts` | типы API каталога, расчётов и анализа с Decimal-значениями в строковом виде |
| `src/shared/api/client.ts` | fetch-клиент API с таймаутом 200 секунд и разбором ошибок 422 с issues |
| `src/features/simulator/useSimulator.ts` | состояние симулятора: каталог, выбор пяти районов, бюджет, расчёты API, AI-результаты и сохранения |
| `src/features/simulator/storage.ts` | версионированное localStorage-хранилище до 20 сценариев и проверка формы сценария |
| `src/features/simulator/ScenarioPanel.tsx` | панель выбора мэра и районов, вкладки и сохранённые сценарии |
| `src/features/simulator/ResultsPanel.tsx` | вывод оценки, дельт районов, показателей, синергий и AI-анализа |
| `src/features/simulator/Simulator.module.css` | адаптивная раскладка панелей симулятора |
| `src/pages/MapPage.tsx` | объединение карты и сценария, показатель города, карточки пяти районов и ориентиры |
| `src/pages/MapPage.module.css` | адаптивное оформление общего экрана карты и сценария |
| `src/shared/ui/Icon.tsx` | SVG-иконки общего пользовательского интерфейса |
| `src/shared/ui/ErrorBoundary.tsx` | экран ошибки React-приложения |
| `src/styles/global.css` | базовые стили и переопределения MapLibre |
| `tests/production.test.mjs` | регрессионная проверка отсутствующего worker в production |

## deploy/
| Файл | Отвечает за |
|---|---|
| `nginx/nginx.conf` | раздача статики, `/health` и same-origin проксирование `/api` в `api:8000` через Docker DNS с timeout 200 секунд |

## Общая инфраструктура

| Файл | Отвечает за |
|---|---|
| `docker-compose.yml` | клиент, включение core/server Compose, ожидание здоровья API |
| `.env.example` | порты 8040/8050, пустой ключ OpenAI, модель gpt-6-sol |
| `Makefile` | запуск всего стека, проверки API и ядра, CLI; preview как alias up |
| `docker-compose.preview.yml` | пустой совместимый override; соседние клоны main не нужны |
