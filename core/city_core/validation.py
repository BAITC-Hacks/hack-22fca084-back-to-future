"""Все ограничения сценария; вычисления Score здесь не выполняются."""

from collections import Counter
from collections.abc import Sequence

from .catalog import get_catalog
from .models import Selection, ValidationIssue


def validate_scenario(selections: Sequence[Selection]) -> tuple[ValidationIssue, ...]:
    catalog = get_catalog()
    measures = {item.id: item for item in catalog.measures}
    districts = {item.id for item in catalog.districts}
    issues: list[ValidationIssue] = []
    if len(selections) != catalog.required_selections:
        issues.append(ValidationIssue("selection_count", "Нужно выбрать ровно 5 мероприятий."))

    counts = Counter(item.measure_id for item in selections)
    for measure_id, count in sorted(counts.items()):
        if count > 1:
            issues.append(
                ValidationIssue("duplicate_measure", "Мероприятие нельзя повторять.", (measure_id,))
            )

    for selected in sorted(selections, key=lambda item: (item.measure_id, item.district_id or "")):
        measure = measures.get(selected.measure_id)
        if measure is None:
            issues.append(
                ValidationIssue(
                    "unknown_measure", "Неизвестное мероприятие.", (selected.measure_id,)
                )
            )
            continue
        if measure.scope == "city" and selected.district_id is not None:
            issues.append(
                ValidationIssue(
                    "unexpected_district", "Для городской меры район не нужен.", (measure.id,)
                )
            )
        if measure.scope == "district":
            if selected.district_id is None:
                issues.append(
                    ValidationIssue(
                        "district_required", "Укажите район мероприятия.", (measure.id,)
                    )
                )
            elif selected.district_id not in districts:
                issues.append(
                    ValidationIssue("unknown_district", "Неизвестный район.", (measure.id,))
                )

    known = [measures[item.measure_id] for item in selections if item.measure_id in measures]
    spent = sum(item.cost for item in known)
    if spent > catalog.budget:
        issues.append(ValidationIssue("budget_exceeded", f"Бюджет превышен: {spent} из 100."))
    for direction, count in sorted(Counter(item.direction for item in known).items()):
        if count > catalog.max_per_direction:
            affected = tuple(sorted(item.id for item in known if item.direction == direction))
            issues.append(
                ValidationIssue(
                    "direction_limit", "Не более двух мер одного направления.", affected
                )
            )

    for conflict in catalog.conflicts:
        first = [item for item in selections if item.measure_id == conflict.measure_ids[0]]
        second = [item for item in selections if item.measure_id == conflict.measure_ids[1]]
        if (
            first
            and second
            and (
                conflict.scope == "global"
                or any(
                    a.district_id in districts and a.district_id == b.district_id
                    for a in first
                    for b in second
                )
            )
        ):
            issues.append(
                ValidationIssue("incompatible_measures", conflict.reason, conflict.measure_ids)
            )
    return tuple(issues)
