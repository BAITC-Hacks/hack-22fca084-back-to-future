"""Преобразование HTTP-схем в типы ядра без дублирования формул или каталога."""

from city_core import Selection, baseline, evaluate_scenario, get_catalog

from .schemas import CatalogResponse, EvaluateRequest, EvaluateResponse


def read_catalog() -> CatalogResponse:
    return CatalogResponse(catalog=get_catalog(), baseline=baseline())


def evaluate(request: EvaluateRequest) -> EvaluateResponse:
    outcome = evaluate_scenario(
        tuple(Selection(item.measure_id, item.district_id) for item in request.selections)
    )
    return EvaluateResponse(issues=outcome.issues, result=outcome.result)
