from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from city_core import Selection, evaluate_scenario, get_catalog


def test_catalog_dimensions_weights_and_shares_match_case() -> None:
    catalog = get_catalog()

    assert (len(catalog.districts), len(catalog.indicators), len(catalog.measures)) == (5, 10, 14)
    assert sum(item.weight for item in catalog.indicators) == 1
    assert sum(item.population_share for item in catalog.districts) == 1
    assert len({item.id for item in catalog.districts}) == 5
    assert len({item.id for item in catalog.indicators}) == 10
    assert len({item.id for item in catalog.measures}) == 14
    indicator_ids = {item.id for item in catalog.indicators}
    assert all(
        {item.indicator_id for item in district.indicators} == indicator_ids
        for district in catalog.districts
    )
    assert all(
        0 <= item.value <= 100 for district in catalog.districts for item in district.indicators
    )
    assert all(0 <= item.lag <= catalog.horizon for item in catalog.measures)
    assert all(
        effect.indicator_id in indicator_ids for item in catalog.measures for effect in item.effects
    )


def test_catalog_cannot_be_mutated_and_is_unchanged_after_calculation(
    example: tuple[Selection, ...],
) -> None:
    catalog = get_catalog()
    field_name = "value"
    with pytest.raises(FrozenInstanceError):
        setattr(catalog.districts[0].indicators[0], field_name, Decimal(0))
    evaluate_scenario(example)

    assert get_catalog() == catalog
    assert get_catalog().districts[0].indicators[0].value == Decimal(45)


@pytest.mark.parametrize(
    "measure_id,cost,lag,effects",
    [
        ("M1", 18, 2, {"T1": 6, "T2": 9}),
        ("M2", 22, 2, {"T1": 4, "B2": 3}),
        ("M3", 30, 4, {"T1": 16, "T2": 20, "E2": 4}),
        ("M4", 15, 2, {"E1": 12, "E2": 3, "B1": 2}),
        ("M5", 25, 3, {"E2": 14, "C1": 4}),
        ("M6", 20, 4, {"E1": 5, "E2": 3}),
        ("M7", 24, 3, {"S1": 16}),
        ("M8", 20, 3, {"S2": 14}),
        ("M9", 10, 1, {"S1": 3, "S2": 3, "B1": 3}),
        ("M10", 12, 1, {"B1": 12, "B2": 2}),
        ("M11", 10, 1, {"B2": 12, "T1": -2}),
        ("M12", 14, 1, {"C2": 5}),
        ("M13", 28, 4, {"C1": 18, "E2": 2}),
        ("M14", 16, 1, {"C1": 5, "C2": 2}),
    ],
)
def test_measure_data_matches_source_document(
    measure_id: str,
    cost: int,
    lag: int,
    effects: dict[str, int],
) -> None:
    measure = next(item for item in get_catalog().measures if item.id == measure_id)

    assert (measure.cost, measure.lag) == (cost, lag)
    assert {item.indicator_id: item.value for item in measure.effects} == effects
