from dataclasses import replace
from decimal import Decimal, localcontext
from itertools import permutations

import pytest

from city_core import Selection, baseline, calculator, evaluate_scenario, get_catalog
from city_core.models import Evaluation, IndicatorValue


def calculate(choices: tuple[Selection, ...]) -> Evaluation:
    outcome = evaluate_scenario(choices)
    assert outcome.result is not None, outcome.issues
    return outcome.result


def test_baseline_matches_case_exactly() -> None:
    city = baseline()

    assert [item.score for item in city.districts] == list(
        map(Decimal, ["62.99", "57.06", "54.65", "56.63", "49.18"])
    )
    assert city.weighted_average == Decimal("56.8624")
    assert city.critical_count == 2
    assert city.score == Decimal("52.55768")


def test_case_example_exact_score_and_districts(example: tuple[Selection, ...]) -> None:
    result = calculate(example)

    assert result.spent == 95
    assert result.remaining == 5
    assert result.after.score == Decimal("56.54307")
    assert result.score_delta == Decimal("3.98539")
    assert result.after.critical_count == 0
    assert result.after.weighted_average == Decimal("58.0776")
    assert [item.score for item in result.after.districts] == list(
        map(Decimal, ["63.4275", "57.4975", "56.3", "57.0675", "52.9625"])
    )


def test_every_permutation_produces_identical_result(example: tuple[Selection, ...]) -> None:
    expected = calculate(example)

    for choices in permutations(example):
        assert calculate(choices) == expected


def test_caller_decimal_precision_cannot_change_score(example: tuple[Selection, ...]) -> None:
    with localcontext() as context:
        context.prec = 3
        result = calculate(example)
        initial = baseline()

    assert result.after.score == Decimal("56.54307")
    assert initial.score == Decimal("52.55768")


@pytest.mark.parametrize(
    "pair,indicator,target,value",
    [
        (("M1", "M2"), "T1", "esil", "2"),
        (("M5", "M6"), "E2", "esil", "2"),
        (("M10", "M12"), "B1", "nura", "2"),
    ],
)
def test_synergy_is_fixed_and_applies_only_to_first_district(
    pair: tuple[str, str],
    indicator: str,
    target: str,
    value: str,
) -> None:
    if pair == ("M10", "M12"):
        choices = (
            Selection("M7", "nura"),
            Selection("M8", "nura"),
            Selection("M10", "nura"),
            Selection("M12"),
            Selection("M5", "saryarka"),
        )
    else:
        choices = (
            Selection(pair[0], target),
            Selection(pair[1]),
            Selection("M9", "nura"),
            Selection("M10", "nura"),
            Selection("M12"),
        )
    result = calculate(choices)

    matches = [
        item for item in result.contributions if item.kind == "synergy" and item.measure_ids == pair
    ]
    assert len(matches) == 1
    assert (matches[0].district_id, matches[0].indicator_id, matches[0].raw_delta) == (
        target,
        indicator,
        Decimal(value),
    )


def test_city_effect_reaches_all_five_districts(example: tuple[Selection, ...]) -> None:
    result = calculate(example)

    effects = [item for item in result.contributions if item.measure_ids == ("M12",)]
    assert {item.district_id for item in effects} == {item.id for item in get_catalog().districts}
    assert all(item.raw_delta == Decimal("4.375") for item in effects)


def test_district_effect_does_not_spread(example: tuple[Selection, ...]) -> None:
    result = calculate(example)

    schools = [item for item in result.changes if item.indicator_id == "S1"]
    assert {item.district_id: item.delta for item in schools} == {
        "esil": Decimal(0),
        "almaty": Decimal(0),
        "saryarka": Decimal(0),
        "baikonur": Decimal(0),
        "nura": Decimal(10),
    }


def test_negative_effect_can_create_new_critical_indicator() -> None:
    result = calculate(
        (
            Selection("M9", "nura"),
            Selection("M11", "almaty"),
            Selection("M10", "nura"),
            Selection("M12"),
            Selection("M4", "saryarka"),
        )
    )

    transport = next(
        item
        for item in result.changes
        if item.district_id == "almaty" and item.indicator_id == "T1"
    )
    assert transport.after == Decimal("38.25")
    assert transport.delta == Decimal("-1.75")
    assert result.after.critical_count == 2
    assert result.spent == 61


@pytest.mark.parametrize("start,expected", [("200", "100"), ("-20", "0"), ("2", "0.25")])
def test_clipping_happens_after_all_effects(
    monkeypatch: pytest.MonkeyPatch,
    start: str,
    expected: str,
) -> None:
    catalog = get_catalog()
    district = catalog.districts[0]
    altered = replace(
        district,
        indicators=tuple(
            IndicatorValue(item.indicator_id, Decimal(start)) if item.indicator_id == "T1" else item
            for item in district.indicators
        ),
    )
    monkeypatch.setattr(
        calculator,
        "get_catalog",
        lambda: replace(catalog, districts=(altered, *catalog.districts[1:])),
    )
    # WHY: крайние значения недостижимы в исходном датасете, но clip — правило кейса.
    result = calculate(
        (
            Selection("M11", "esil"),
            Selection("M9", "nura"),
            Selection("M10", "nura"),
            Selection("M12"),
            Selection("M4", "saryarka"),
        )
    )
    transport = next(
        item for item in result.after.districts[0].indicators if item.indicator_id == "T1"
    )
    assert transport.value == Decimal(expected)


def test_positive_and_negative_effects_are_combined_before_clipping(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog = get_catalog()
    first = catalog.districts[0]
    changed = replace(
        first,
        indicators=tuple(
            replace(item, value=Decimal(99)) if item.indicator_id == "T1" else item
            for item in first.indicators
        ),
    )
    monkeypatch.setattr(
        calculator,
        "get_catalog",
        lambda: replace(catalog, districts=(changed, *catalog.districts[1:])),
    )
    result = calculate(
        (
            Selection("M2"),
            Selection("M11", "esil"),
            Selection("M9", "nura"),
            Selection("M12"),
            Selection("M4", "saryarka"),
        )
    )

    transport = next(
        item for item in result.after.districts[0].indicators if item.indicator_id == "T1"
    )
    assert transport.value == Decimal(100)


@pytest.mark.parametrize("value,count", [("39.999", 3), ("40", 2), ("40.001", 2)])
def test_critical_threshold_is_strict(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
    count: int,
) -> None:
    catalog = get_catalog()
    first = catalog.districts[0]
    changed = replace(
        first,
        indicators=tuple(
            replace(item, value=Decimal(value)) if item.indicator_id == "T1" else item
            for item in first.indicators
        ),
    )
    monkeypatch.setattr(
        calculator,
        "get_catalog",
        lambda: replace(catalog, districts=(changed, *catalog.districts[1:])),
    )

    assert baseline().critical_count == count


def test_contributions_reconcile_with_indicator_changes(example: tuple[Selection, ...]) -> None:
    result = calculate(example)

    for change in result.changes:
        total = sum(
            (
                item.raw_delta
                for item in result.contributions
                if item.district_id == change.district_id
                and item.indicator_id == change.indicator_id
            ),
            Decimal(0),
        )
        assert change.after == max(Decimal(0), min(Decimal(100), change.before + total))


def test_district_score_deltas_are_computed_for_ai(example: tuple[Selection, ...]) -> None:
    result = calculate(example)

    assert {item.district_id: item.delta for item in result.district_changes} == {
        "esil": Decimal("0.4375"),
        "almaty": Decimal("0.4375"),
        "saryarka": Decimal("1.65"),
        "baikonur": Decimal("0.4375"),
        "nura": Decimal("3.7825"),
    }
