# Карта кода

**Обновлена:** 2026-09-23

## Корень проекта
| Файл | Отвечает за |
|---|---|
| `.env.example` | шаблон `CLIENT_PORT`, пустого `OPENAI_API_KEY` и модели `OPENAI_MODEL=gpt-6-sol` |
| `Makefile` | команды управления стеком, включая `make preview` для preview-сборки |
| `docker-compose.yml` | запуск одного клиентского сервиса, публикация `CLIENT_PORT` и healthcheck |
| `docker-compose.preview.yml` | preview-overrides: сборка API из соседнего `../alisher/server/Dockerfile`, передача ключа только API и зависимость клиента от healthy API |

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
