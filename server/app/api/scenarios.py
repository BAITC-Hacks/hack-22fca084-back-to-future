from fastapi import APIRouter, Response

from .. import core_adapter
from ..schemas import EvaluateRequest, EvaluateResponse, InputErrorResponse

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.post(
    "/evaluate",
    response_model=EvaluateResponse,
    responses={422: {"model": EvaluateResponse | InputErrorResponse}},
    summary="Проверить пять решений и рассчитать Score",
)
def evaluate(request: EvaluateRequest, response: Response) -> EvaluateResponse:
    outcome = core_adapter.evaluate(request)
    if outcome.result is None:
        response.status_code = 422
    return outcome
