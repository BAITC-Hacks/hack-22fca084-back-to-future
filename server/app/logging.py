"""Идентификатор и JSON-журнал запроса; тело и секреты в журнал не попадают."""

import json
import logging
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("astana.requests")


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid4())
        started = perf_counter()
        try:
            response = await call_next(request)
        except Exception as error:
            # WHY: граница HTTP скрывает внутреннюю ошибку и фиксирует её ровно один раз.
            logger.error(
                json.dumps(
                    {
                        "event": "request_failed",
                        "request_id": request_id,
                        "error_type": type(error).__name__,
                    }
                )
            )
            response = JSONResponse(
                status_code=500,
                content={
                    "issues": [
                        {"code": "internal_error", "message": "Не удалось обработать запрос."}
                    ],
                    "result": None,
                },
            )
        response.headers["X-Request-ID"] = request_id
        logger.info(
            json.dumps(
                {
                    "event": "request_completed",
                    "request_id": request_id,
                    "method": request.method,
                    "status": response.status_code,
                    "duration_ms": round((perf_counter() - started) * 1000, 2),
                }
            )
        )
        return response
