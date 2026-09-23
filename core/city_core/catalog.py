"""Синтетический датасет кейса «Аким на 5 часов».

Владеет исходными числами и ограничениями; не считает результаты сценариев.
INVARIANT: десятичные константы создаются из строк, все коллекции неизменяемы.
"""

from decimal import Decimal

from .models import Catalog, Conflict, District, Indicator, IndicatorValue, Measure, Synergy


def _values(**values: int) -> tuple[IndicatorValue, ...]:
    return tuple(IndicatorValue(key, Decimal(value)) for key, value in values.items())


_CATALOG = Catalog(
    version="case-v1",
    budget=100,
    required_selections=5,
    max_per_direction=2,
    horizon=8,
    indicators=(
        Indicator("T1", "Разгрузка дорог", "transport", Decimal("0.10")),
        Indicator("T2", "Доступность общественного транспорта", "transport", Decimal("0.10")),
        Indicator("E1", "Озеленение", "ecology", Decimal("0.09")),
        Indicator("E2", "Качество воздуха", "ecology", Decimal("0.11")),
        Indicator("S1", "Школы и детсады", "social", Decimal("0.11")),
        Indicator("S2", "Поликлиники и первичная медпомощь", "social", Decimal("0.11")),
        Indicator("B1", "Безопасность улиц", "safety", Decimal("0.09")),
        Indicator("B2", "Безопасность дорожного движения", "safety", Decimal("0.09")),
        Indicator("C1", "Надёжность ЖКХ", "services", Decimal("0.10")),
        Indicator("C2", "Скорость решения обращений жителей", "services", Decimal("0.10")),
    ),
    districts=(
        District(
            "esil",
            "Есиль",
            Decimal("0.27"),
            "Богатый район, но с пробками на мостах и переполненными школами.",
            _values(T1=45, T2=62, E1=68, E2=72, S1=48, S2=55, B1=78, B2=60, C1=75, C2=70),
        ),
        District(
            "almaty",
            "Алматы",
            Decimal("0.24"),
            "Старый ЖКХ и пробки.",
            _values(T1=40, T2=75, E1=50, E2=55, S1=60, S2=65, B1=62, B2=52, C1=50, C2=60),
        ),
        District(
            "saryarka",
            "Сарыарка",
            Decimal("0.20"),
            "Смог от частного сектора, слабое озеленение.",
            _values(T1=50, T2=70, E1=42, E2=40, S1=62, S2=68, B1=58, B2=55, C1=45, C2=55),
        ),
        District(
            "baikonur",
            "Байконур",
            Decimal("0.13"),
            "Середняк без ярких перекосов.",
            _values(T1=52, T2=68, E1=55, E2=50, S1=58, S2=60, B1=52, B2=58, C1=55, C2=58),
        ),
        District(
            "nura",
            "Нура",
            Decimal("0.16"),
            "Главный аутсайдер по соцсфере и транспорту.",
            _values(T1=55, T2=40, E1=45, E2=65, S1=38, S2=35, B1=55, B2=50, C1=60, C2=50),
        ),
    ),
    measures=(
        Measure(
            "M1",
            "Выделенные полосы для автобусов",
            "transport",
            "district",
            18,
            2,
            _values(T1=6, T2=9),
        ),
        Measure(
            "M2",
            "Умные светофоры (адаптивное управление)",
            "transport",
            "city",
            22,
            2,
            _values(T1=4, B2=3),
        ),
        Measure(
            "M3",
            "Линия ЛРТ / расширение",
            "transport",
            "district",
            30,
            4,
            _values(T1=16, T2=20, E2=4),
        ),
        Measure("M4", "Парк / сквер", "ecology", "district", 15, 2, _values(E1=12, E2=3, B1=2)),
        Measure(
            "M5",
            "Перевод частного сектора на чистое топливо",
            "ecology",
            "district",
            25,
            3,
            _values(E2=14, C1=4),
        ),
        Measure(
            "M6",
            "Городская программа озеленения и ветрозащитных полос",
            "ecology",
            "city",
            20,
            4,
            _values(E1=5, E2=3),
        ),
        Measure(
            "M7",
            "Школа + детсад (модульное строительство)",
            "social",
            "district",
            24,
            3,
            _values(S1=16),
        ),
        Measure(
            "M8",
            "Центр семейного здоровья / поликлиника",
            "social",
            "district",
            20,
            3,
            _values(S2=14),
        ),
        Measure(
            "M9", "Дворовые спорт-хабы", "social", "district", 10, 1, _values(S1=3, S2=3, B1=3)
        ),
        Measure(
            "M10",
            "Освещение и камеры (расширение Safe City)",
            "safety",
            "district",
            12,
            1,
            _values(B1=12, B2=2),
        ),
        Measure(
            "M11",
            "Безопасные переходы и школьные зоны",
            "safety",
            "district",
            10,
            1,
            _values(B2=12, T1=-2),
        ),
        Measure(
            "M12", "Единая цифровая платформа обращений", "services", "city", 14, 1, _values(C2=5)
        ),
        Measure(
            "M13",
            "Модернизация тепло- и водосетей",
            "services",
            "district",
            28,
            4,
            _values(C1=18, E2=2),
        ),
        Measure(
            "M14",
            "Аварийные бригады ЖКХ + раннее оповещение",
            "services",
            "city",
            16,
            1,
            _values(C1=5, C2=2),
        ),
    ),
    synergies=(
        Synergy(("M1", "M2"), IndicatorValue("T1", Decimal(2))),
        Synergy(("M10", "M12"), IndicatorValue("B1", Decimal(2))),
        Synergy(("M5", "M6"), IndicatorValue("E2", Decimal(2))),
    ),
    conflicts=(
        Conflict(("M1", "M3"), "global", "Выберите либо автобусные полосы, либо ЛРТ."),
        Conflict(
            ("M4", "M7"), "same_district", "Парк и школа конфликтуют за участок в одном районе."
        ),
        Conflict(
            ("M5", "M13"),
            "same_district",
            "Чистое топливо и модернизация сетей дублируют программу в одном районе.",
        ),
    ),
)


def get_catalog() -> Catalog:
    return _CATALOG
