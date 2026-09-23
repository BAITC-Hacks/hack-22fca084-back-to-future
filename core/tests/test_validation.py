from collections.abc import Sequence

import pytest

from city_core import Selection, evaluate_scenario, validate_scenario


def scenario(*ids: str) -> tuple[Selection, ...]:
    return tuple(
        Selection(item, None if item in {"M2", "M6", "M12", "M14"} else "nura") for item in ids
    )


@pytest.mark.parametrize(
    "selections,code",
    [
        ((), "selection_count"),
        (scenario("M7", "M8", "M10", "M12"), "selection_count"),
        (scenario("M7", "M8", "M10", "M12", "M5", "M14"), "selection_count"),
        (
            (
                Selection("M7", "nura"),
                Selection("M7", "esil"),
                Selection("M10", "nura"),
                Selection("M12"),
                Selection("M5", "saryarka"),
            ),
            "duplicate_measure",
        ),
        (scenario("M3", "M5", "M7", "M10", "M9"), "budget_exceeded"),
        (scenario("M7", "M8", "M9", "M10", "M12"), "direction_limit"),
        (scenario("M1", "M3", "M9", "M10", "M12"), "incompatible_measures"),
        (scenario("M4", "M7", "M9", "M10", "M12"), "incompatible_measures"),
        (scenario("M5", "M13", "M9", "M10", "M12"), "incompatible_measures"),
        (scenario("bad", "M8", "M10", "M12", "M5"), "unknown_measure"),
        ((Selection("M7"), *scenario("M8", "M10", "M12", "M5")), "district_required"),
        ((Selection("M7", "unknown"), *scenario("M8", "M10", "M12", "M5")), "unknown_district"),
        ((Selection("M12", "nura"), *scenario("M7", "M8", "M10", "M5")), "unexpected_district"),
    ],
)
def test_invalid_scenarios_never_receive_score(selections: Sequence[Selection], code: str) -> None:
    outcome = evaluate_scenario(selections)

    assert outcome.result is None
    assert code in {item.code for item in outcome.issues}


def test_global_conflict_applies_across_districts() -> None:
    choices = (Selection("M1", "nura"), Selection("M3", "esil"), *scenario("M9", "M10", "M12"))

    assert "incompatible_measures" in {item.code for item in validate_scenario(choices)}


@pytest.mark.parametrize("pair", [("M4", "M7"), ("M5", "M13")])
def test_local_conflicts_allow_different_districts(pair: tuple[str, str]) -> None:
    choices = (
        Selection(pair[0], "nura"),
        Selection(pair[1], "esil"),
        *scenario("M9", "M10", "M12"),
    )

    assert not validate_scenario(choices)


def test_exact_budget_is_valid() -> None:
    outcome = evaluate_scenario(scenario("M3", "M7", "M8", "M10", "M12"))

    assert outcome.result is not None
    assert outcome.result.spent == 100
    assert outcome.result.remaining == 0


def test_validation_returns_multiple_reasons() -> None:
    issues = validate_scenario((Selection("M7"), Selection("M7", "unknown")))

    assert {item.code for item in issues} == {
        "selection_count",
        "duplicate_measure",
        "district_required",
        "unknown_district",
    }
