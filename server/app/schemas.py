"""Строгий HTTP-контракт; данные результатов остаются типами ядра."""

from pydantic import BaseModel, ConfigDict, Field

from city_core.models import Catalog, CityResult, Evaluation, ValidationIssue


class SelectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    measure_id: str = Field(min_length=1, max_length=16)
    district_id: str | None = Field(default=None, max_length=32)


class EvaluateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    selections: list[SelectionRequest] = Field(max_length=32)


class EvaluateResponse(BaseModel):
    issues: tuple[ValidationIssue, ...]
    result: Evaluation | None


class CatalogResponse(BaseModel):
    catalog: Catalog
    baseline: CityResult


class InputIssue(BaseModel):
    code: str
    message: str
    location: tuple[str, ...]


class InputErrorResponse(BaseModel):
    issues: tuple[InputIssue, ...]
    result: None = None
