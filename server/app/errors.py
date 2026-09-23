"""Ошибки формы запроса без эха входных данных и внутренних деталей."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from .schemas import InputErrorResponse, InputIssue


async def invalid_request(request: Request, error: RequestValidationError) -> JSONResponse:
    response = InputErrorResponse(
        issues=tuple(
            InputIssue(
                code="invalid_input",
                message="Некорректный формат поля запроса.",
                location=tuple(str(part) for part in item["loc"]),
            )
            for item in error.errors()
        )
    )
    return JSONResponse(status_code=422, content=response.model_dump(mode="json"))
