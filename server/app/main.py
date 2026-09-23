"""Сборка FastAPI: маршруты, обработчик валидации и журнал запросов."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .api.analysis import router as analysis_router
from .api.catalog import router as catalog_router
from .api.health import router as health_router
from .api.scenarios import router as scenarios_router
from .config import Settings
from .errors import invalid_request
from .logging import RequestLogMiddleware, configure_logging


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    settings = Settings()
    application.state.settings = settings
    application.state.analysis_slots = asyncio.Semaphore(2)
    async with httpx.AsyncClient(
        timeout=settings.openai_timeout_seconds, trust_env=False
    ) as client:
        application.state.http = client
        yield


def create_app() -> FastAPI:
    configure_logging()
    application = FastAPI(title="Аким на 5 часов", version="0.1.0", lifespan=lifespan)
    application.add_middleware(RequestLogMiddleware)
    application.exception_handler(RequestValidationError)(invalid_request)
    application.include_router(health_router)
    application.include_router(catalog_router)
    application.include_router(scenarios_router)
    application.include_router(analysis_router)
    return application


app = create_app()
