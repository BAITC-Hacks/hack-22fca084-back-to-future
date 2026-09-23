# Проверка ядра без интерфейса

Из корня клона с Docker Compose:

```bash
make core-check
make up
docker compose logs core
```

`core` — одноразовый CLI-контейнер. После расчёта штатно завершается с кодом 0.
Он не открывает порт и не нуждается в доступе к сети во время выполнения.

Отдельные операции:

```bash
docker compose run --rm -T core python -m city_core baseline
docker compose run --rm -T core python -m city_core catalog
docker compose run --rm -T core python -m city_core demo
docker compose run --rm -T core python -m city_core evaluate < core/tests/fixtures/example_95.json
docker compose run --rm -T core python -m city_core evaluate < core/tests/fixtures/over_budget.json
```

Последний пример намеренно превышает бюджет: код выхода 2, `budget_exceeded`,
`result: null`. Это ожидаемый отказ, а не ошибка расчётного сервиса.
Остальные возвращают код 0 и JSON.

Контрольные значения без округления:

| Показатель | База | Пример за 95 |
|---|---:|---:|
| Средневзвешенный балл | 56.8624 | 58.0776 |
| Худший район | 49.18 | 52.9625 |
| Критические показатели | 2 | 0 |
| Score | 52.55768 | 56.54307 |

Результат содержит `district_changes` (дельты районных баллов), `changes`
(дельты показателей) и `contributions` (вклады до clip). Значения Decimal
передаются строками для сохранения точности.
