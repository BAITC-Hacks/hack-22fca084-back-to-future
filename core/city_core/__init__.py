"""Публичная граница расчётного ядра; без внешних зависимостей."""

from .calculator import baseline, evaluate_scenario
from .catalog import get_catalog
from .models import EvaluationOutcome, Selection
from .validation import validate_scenario

__all__ = [
    "EvaluationOutcome",
    "Selection",
    "baseline",
    "evaluate_scenario",
    "get_catalog",
    "validate_scenario",
]
