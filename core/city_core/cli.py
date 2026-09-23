"""Контейнерный CLI библиотеки; evaluate читает JSON из stdin."""

import argparse
import json
import sys

from .calculator import baseline, evaluate_scenario
from .catalog import get_catalog
from .models import Selection
from .serialization import parse_selections, to_json_value


def main() -> int:
    parser = argparse.ArgumentParser(description="Расчёт симулятора Астаны")
    parser.add_argument("command", choices=("catalog", "baseline", "demo", "evaluate"))
    args = parser.parse_args()
    if args.command == "catalog":
        print(json.dumps(to_json_value(get_catalog()), ensure_ascii=False, indent=2))
        return 0
    if args.command == "baseline":
        print(json.dumps(to_json_value(baseline()), ensure_ascii=False, indent=2))
        return 0
    choices: tuple[Selection, ...]
    if args.command == "demo":
        choices = (
            Selection("M7", "nura"),
            Selection("M8", "nura"),
            Selection("M10", "nura"),
            Selection("M12"),
            Selection("M5", "saryarka"),
        )
    else:
        try:
            choices = parse_selections(json.load(sys.stdin))
        except (ValueError, UnicodeError) as error:
            print(
                json.dumps(
                    {"issues": [{"code": "invalid_input", "message": str(error)}], "result": None},
                    ensure_ascii=False,
                )
            )
            return 2
    outcome = evaluate_scenario(choices)
    print(json.dumps(to_json_value(outcome), ensure_ascii=False, indent=2))
    return 0 if outcome.result is not None else 2
