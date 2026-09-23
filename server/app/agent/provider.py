"""Один ограниченный вызов OpenAI; без арифметики и HTTP-ошибок наружу."""

import json
from pathlib import Path

import httpx
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from ..config import Settings
from ..schemas import CatalogResponse, EvaluateResponse


class Analysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str
    strengths: list[str]
    risks: list[str]
    consequences: list[str]
    recommendations: list[str]

    @field_validator("summary", "strengths", "risks", "consequences", "recommendations")
    @classmethod
    def no_invented_numbers(cls, value: str | list[str]) -> str | list[str]:
        texts = [value] if isinstance(value, str) else value
        if any(not text.strip() or any(char.isdecimal() for char in text) for text in texts):
            raise ValueError("Analysis must contain nonempty narrative without numeric claims")
        return value


class ProviderError(Exception):
    pass


async def explain(
    client: httpx.AsyncClient,
    settings: Settings,
    catalog: CatalogResponse,
    outcome: EvaluateResponse,
) -> Analysis:
    prompt = Path(__file__).with_name("prompt.md").read_text(encoding="utf-8")
    payload = {
        "model": settings.openai_model,
        "max_completion_tokens": 4000,
        "service_tier": "flex",
        "reasoning_effort": "low",
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "catalog": catalog.model_dump(mode="json"),
                        "outcome": outcome.model_dump(mode="json"),
                    },
                    ensure_ascii=False,
                ),
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "city_analysis",
                "strict": True,
                "schema": Analysis.model_json_schema(),
            },
        },
    }
    try:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers={"Authorization": "Bearer " + settings.openai_api_key.get_secret_value()},
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise ProviderError("Provider did not return text")
        return Analysis.model_validate_json(content)
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError, ValidationError) as error:
        raise ProviderError("Provider analysis unavailable") from error
