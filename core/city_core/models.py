"""Неизменяемые данные каталога и результаты расчёта; без HTTP и хранения."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal


@dataclass(frozen=True, slots=True)
class IndicatorValue:
    indicator_id: str
    value: Decimal


@dataclass(frozen=True, slots=True)
class Indicator:
    id: str
    name: str
    direction: str
    weight: Decimal


@dataclass(frozen=True, slots=True)
class District:
    id: str
    name: str
    population_share: Decimal
    profile: str
    indicators: tuple[IndicatorValue, ...]


@dataclass(frozen=True, slots=True)
class Measure:
    id: str
    name: str
    direction: str
    scope: Literal["district", "city"]
    cost: int
    lag: int
    effects: tuple[IndicatorValue, ...]


@dataclass(frozen=True, slots=True)
class Synergy:
    measure_ids: tuple[str, str]
    effect: IndicatorValue


@dataclass(frozen=True, slots=True)
class Conflict:
    measure_ids: tuple[str, str]
    scope: Literal["same_district", "global"]
    reason: str


@dataclass(frozen=True, slots=True)
class Catalog:
    version: str
    budget: int
    required_selections: int
    max_per_direction: int
    horizon: int
    indicators: tuple[Indicator, ...]
    districts: tuple[District, ...]
    measures: tuple[Measure, ...]
    synergies: tuple[Synergy, ...]
    conflicts: tuple[Conflict, ...]


@dataclass(frozen=True, slots=True)
class Selection:
    measure_id: str
    district_id: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str
    measure_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DistrictResult:
    district_id: str
    indicators: tuple[IndicatorValue, ...]
    score: Decimal


@dataclass(frozen=True, slots=True)
class CityResult:
    districts: tuple[DistrictResult, ...]
    weighted_average: Decimal
    weakest_score: Decimal
    critical_count: int
    score: Decimal


@dataclass(frozen=True, slots=True)
class Contribution:
    kind: Literal["measure", "synergy"]
    measure_ids: tuple[str, ...]
    district_id: str
    indicator_id: str
    raw_delta: Decimal


@dataclass(frozen=True, slots=True)
class IndicatorChange:
    district_id: str
    indicator_id: str
    before: Decimal
    after: Decimal
    delta: Decimal


@dataclass(frozen=True, slots=True)
class DistrictChange:
    district_id: str
    before: Decimal
    after: Decimal
    delta: Decimal


@dataclass(frozen=True, slots=True)
class Evaluation:
    selections: tuple[Selection, ...]
    spent: int
    remaining: int
    before: CityResult
    after: CityResult
    score_delta: Decimal
    changes: tuple[IndicatorChange, ...]
    district_changes: tuple[DistrictChange, ...]
    contributions: tuple[Contribution, ...]


@dataclass(frozen=True, slots=True)
class EvaluationOutcome:
    issues: tuple[ValidationIssue, ...]
    result: Evaluation | None
