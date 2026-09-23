import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

from city_core.serialization import parse_selections, to_json_value


def run_cli(command: str, data: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "city_core", command],
        input=data,
        text=True,
        capture_output=True,
        check=False,
    )


def test_baseline_cli_serializes_exact_decimal() -> None:
    process = run_cli("baseline")

    assert process.returncode == 0
    assert json.loads(process.stdout)["score"] == "52.55768"


def test_demo_cli_matches_input_fixture() -> None:
    data = (Path(__file__).parent / "fixtures/example_95.json").read_text()
    demo = run_cli("demo")
    evaluated = run_cli("evaluate", data)

    assert demo.returncode == evaluated.returncode == 0
    assert json.loads(demo.stdout) == json.loads(evaluated.stdout)
    assert Decimal(json.loads(demo.stdout)["result"]["after"]["score"]) == Decimal("56.54307")


@pytest.mark.parametrize(
    "data,code",
    [
        ('{"selections":[]}', "selection_count"),
        ('{"selections":[{"measure_id":5}]}', "invalid_input"),
        ('{"selections":[{"measure_id":"M1","district_id":5}]}', "invalid_input"),
        ('{"selections":[{"measure_id":"M1","cost":0}]}', "invalid_input"),
        ('{"selections":{}}', "invalid_input"),
        ("[]", "invalid_input"),
        ("not json", "invalid_input"),
    ],
)
def test_cli_invalid_input_never_returns_a_score(data: str, code: str) -> None:
    process = run_cli("evaluate", data)

    assert process.returncode == 2
    output = json.loads(process.stdout)
    assert output["result"] is None
    assert code in {item["code"] for item in output["issues"]}
    assert not process.stderr


def test_cli_reports_budget_exceeded() -> None:
    data = (Path(__file__).parent / "fixtures/over_budget.json").read_text()
    process = run_cli("evaluate", data)

    assert process.returncode == 2
    assert "budget_exceeded" in {item["code"] for item in json.loads(process.stdout)["issues"]}


def test_catalog_cli_is_serializable_and_contains_constraints() -> None:
    process = run_cli("catalog")

    assert process.returncode == 0
    catalog = json.loads(process.stdout)
    assert catalog["budget"] == 100
    assert len(catalog["conflicts"]) == len(catalog["synergies"]) == 3


def test_decimal_serialization_never_rounds() -> None:
    assert to_json_value(Decimal("0.1234567890123456789")) == "0.1234567890123456789"


@pytest.mark.parametrize(
    "value", [{"selections": None}, {"selections": [None]}, {"selections": [{"measure_id": ""}]}]
)
def test_parser_rejects_wrong_shapes(value: object) -> None:
    with pytest.raises(ValueError):
        parse_selections(value)
