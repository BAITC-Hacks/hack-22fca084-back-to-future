"""JSON-граница библиотеки: Decimal сохраняется точной десятичной строкой."""

from dataclasses import fields, is_dataclass
from decimal import Decimal

from .models import Selection

type JsonValue = str | int | bool | None | list[JsonValue] | dict[str, JsonValue]


def to_json_value(value: object) -> JsonValue:
    if isinstance(value, Decimal):
        return format(value, "f")
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: to_json_value(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, (tuple, list)):
        return [to_json_value(item) for item in value]
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise TypeError(f"Unsupported JSON value: {type(value).__name__}")


def parse_selections(value: object) -> tuple[Selection, ...]:
    if not isinstance(value, dict) or set(value) != {"selections"}:
        raise ValueError("Ожидается объект с единственным полем selections.")
    items = value["selections"]
    if not isinstance(items, list):
        raise ValueError("Поле selections должно быть массивом.")
    selections: list[Selection] = []
    for item in items:
        if not isinstance(item, dict) or set(item) - {"measure_id", "district_id"}:
            raise ValueError("Каждое решение содержит только measure_id и district_id.")
        measure_id = item.get("measure_id")
        district_id = item.get("district_id")
        if not isinstance(measure_id, str) or not measure_id:
            raise ValueError("measure_id должен быть непустой строкой.")
        if district_id is not None and not isinstance(district_id, str):
            raise ValueError("district_id должен быть строкой или null.")
        selections.append(Selection(measure_id, district_id))
    return tuple(selections)
