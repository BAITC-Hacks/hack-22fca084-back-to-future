"""Маршрут AI: сначала проверка ядром, затем один вызов модели."""

import asyncio
from typing import Literal

from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from ..agent.provider import Analysis, ProviderError, explain
from ..core_adapter import evaluate, read_catalog
from ..schemas import EvaluateRequest, EvaluateResponse

router = APIRouter(prefix="/api/scenarios", tags=["analysis"])


class AnalysisResponse(BaseModel):
    status: Literal["success", "unavailable", "error", "invalid"]
    message: str
    analysis: Analysis | None = None
    evaluation: EvaluateResponse


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={422: {"model": AnalysisResponse}},
    summary="Объяснить сценарий через OpenAI",
)
async def analyze(
    payload: EvaluateRequest, request: Request, response: Response
) -> AnalysisResponse:
    outcome = evaluate(payload)
    if outcome.result is None:
        response.status_code = 422
        return AnalysisResponse(
            status="invalid", message="Сначала исправьте сценарий.", evaluation=outcome
        )
    settings = request.app.state.settings
    if not settings.openai_api_key.get_secret_value():
        return AnalysisResponse(
            status="unavailable",
            message="AI-анализ ещё не подключён. Расчёт доступен полностью.",
            evaluation=outcome,
        )
    try:
        async with asyncio.timeout(settings.openai_timeout_seconds):
            async with request.app.state.analysis_slots:
                result = await explain(request.app.state.http, settings, read_catalog(), outcome)
        return AnalysisResponse(
            status="success", message="Анализ завершён.", analysis=result, evaluation=outcome
        )
    except (ProviderError, TimeoutError):
        return AnalysisResponse(
            status="error",
            message="Сервис AI сейчас недоступен. Результат расчёта сохранён; попробуйте снова.",
            evaluation=outcome,
        )
