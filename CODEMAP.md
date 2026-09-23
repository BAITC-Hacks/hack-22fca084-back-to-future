# Карта кода

**Обновлена:** 2026-09-23

## Корень проекта
| Файл | Отвечает за |
|---|---|
| `.env.example` | шаблон порта клиентского сервиса: `CLIENT_PORT=8010` |
| `docker-compose.yml` | запуск одного клиентского сервиса, публикация `CLIENT_PORT` и healthcheck |

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
| `src/pages/MapPage.tsx` | композиция карты, панели и подсказок |
| `src/pages/MapPage.module.css` | адаптивное оформление страницы карты |
| `src/shared/ui/Icon.tsx` | SVG-иконки общего пользовательского интерфейса |
| `src/shared/ui/ErrorBoundary.tsx` | экран ошибки React-приложения |
| `src/styles/global.css` | базовые стили и переопределения MapLibre |
| `tests/production.test.mjs` | регрессионная проверка отсутствующего worker в production |

## deploy/
| Файл | Отвечает за |
|---|---|
| `nginx/nginx.conf` | раздача статики, кеширование ассетов и endpoint `/health` |
