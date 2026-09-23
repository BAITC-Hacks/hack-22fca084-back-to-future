# Стек

**Обновлён:** 2026-09-23

## Клиент
- react 19.3.0 — `client/package.json`.
- react-dom 19.3.0 — `client/package.json`.
- maplibre-gl 6.11.1 — `client/package.json`.
- typescript 6.0.3 — `client/package.json`.
- vite 8.3.0 — `client/package.json`.
- eslint 9.39.5 — `client/package.json`.
- CSS Modules — `client/src/pages/MapPage.module.css`.
- OpenFreeMap / OpenStreetMap — внешний источник в `client/src/features/map/mapConfig.ts`.

## Инфраструктура
- Docker Compose — `docker-compose.yml`; Node 22 и Nginx 1.29 Alpine — `client/Dockerfile`.
- Preview — `docker-compose.preview.yml`: сборка FastAPI и ядра из соседнего `../alisher/`, same-origin API через Nginx.
- Сценарии — versioned localStorage (`client/src/features/simulator/storage.ts`); БД и регистрации нет.
- ИИ вызывается только через API: `gpt-6-sol`, Flex, ключ в окружении серверного контейнера.

## Проверенные команды
Все команды выполняются из каталога `mansur/`.

| Проверка | Команда |
|---|---|
| Клиент | `make up` |
| Демо с API из соседнего клона | `make preview` |
| Типы | `npm --prefix client run typecheck` |
| Линтер | `npm --prefix client run lint` |
| Сборка | `npm --prefix client run build` |
| Сборка и регрессия worker | `npm --prefix client run test` |
| Статус контейнера | `docker compose ps` |
| Здоровье | `curl -fsS http://localhost:8010/health` |
