"""Точный расчёт Score и трасса влияний для API и ИИ.

Не владеет HTTP, округлением для экрана или генерацией объяснений.
INVARIANT: сначала суммируются все эффекты, затем clip; синергии без лага.
"""

from collections.abc import Sequence
from decimal import Context, Decimal, localcontext

from .catalog import get_catalog
from .models import (
    CityResult,
    Contribution,
    DistrictChange,
    DistrictResult,
    Evaluation,
    EvaluationOutcome,
    IndicatorChange,
    IndicatorValue,
    Selection,
)
from .validation import validate_scenario


def _contributions(selections: tuple[Selection, ...]) -> tuple[Contribution, ...]:
    catalog = get_catalog()
    measures = {item.id: item for item in catalog.measures}
    selected = {item.measure_id: item for item in selections}
    result: list[Contribution] = []
    for choice in selections:
        measure = measures[choice.measure_id]
        factor = Decimal(catalog.horizon - measure.lag) / Decimal(catalog.horizon)
        targets = (
            (choice.district_id,)
            if choice.district_id is not None
            else tuple(item.id for item in catalog.districts)
        )
        for district_id in targets:
            for effect in measure.effects:
                result.append(
                    Contribution(
                        "measure",
                        (measure.id,),
                        district_id,
                        effect.indicator_id,
                        effect.value * factor,
                    )
                )
    for synergy in catalog.synergies:
        if all(measure_id in selected for measure_id in synergy.measure_ids):
            synergy_district_id = selected[synergy.measure_ids[0]].district_id
            # INVARIANT: первая мера каждой синергии районная, вход уже проверен.
            assert synergy_district_id is not None
            result.append(
                Contribution(
                    "synergy",
                    synergy.measure_ids,
                    synergy_district_id,
                    synergy.effect.indicator_id,
                    synergy.effect.value,
                )
            )
    return tuple(result)


def _city_result(contributions: tuple[Contribution, ...]) -> CityResult:
    catalog = get_catalog()
    weights = {item.id: item.weight for item in catalog.indicators}
    total: dict[tuple[str, str], Decimal] = {}
    for contribution in contributions:
        key = (contribution.district_id, contribution.indicator_id)
        total[key] = total.get(key, Decimal(0)) + contribution.raw_delta

    districts: list[DistrictResult] = []
    weighted_average = Decimal(0)
    critical_count = 0
    for district in catalog.districts:
        indicators = tuple(
            IndicatorValue(
                item.indicator_id,
                max(
                    Decimal(0),
                    min(
                        Decimal(100),
                        item.value + total.get((district.id, item.indicator_id), Decimal(0)),
                    ),
                ),
            )
            for item in district.indicators
        )
        score = sum((item.value * weights[item.indicator_id] for item in indicators), Decimal(0))
        districts.append(DistrictResult(district.id, indicators, score))
        weighted_average += district.population_share * score
        critical_count += sum(item.value < 40 for item in indicators)
    weakest_score = min(item.score for item in districts)
    score = Decimal("0.7") * weighted_average + Decimal("0.3") * weakest_score - critical_count
    return CityResult(tuple(districts), weighted_average, weakest_score, critical_count, score)


def baseline() -> CityResult:
    # WHY: настройки Decimal в вызывающем сервере не должны менять результат кейса.
    with localcontext(Context(prec=28)):
        return _city_result(())


def evaluate_scenario(selections: Sequence[Selection]) -> EvaluationOutcome:
    choices = tuple(selections)
    issues = validate_scenario(choices)
    if issues:
        return EvaluationOutcome(issues, None)
    canonical = tuple(sorted(choices, key=lambda item: (item.measure_id, item.district_id or "")))
    with localcontext(Context(prec=28)):
        contributions = _contributions(canonical)
        before = _city_result(())
        after = _city_result(contributions)
        changes = tuple(
            IndicatorChange(
                old_district.district_id,
                old.indicator_id,
                old.value,
                new.value,
                new.value - old.value,
            )
            for old_district, new_district in zip(before.districts, after.districts, strict=True)
            for old, new in zip(old_district.indicators, new_district.indicators, strict=True)
        )
        district_changes = tuple(
            DistrictChange(old.district_id, old.score, new.score, new.score - old.score)
            for old, new in zip(before.districts, after.districts, strict=True)
        )
        costs = {item.id: item.cost for item in get_catalog().measures}
        spent = sum(costs[item.measure_id] for item in canonical)
        result = Evaluation(
            canonical,
            spent,
            get_catalog().budget - spent,
            before,
            after,
            after.score - before.score,
            changes,
            district_changes,
            contributions,
        )
        return EvaluationOutcome((), result)
