import json
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app import core_adapter
from app.schemas import EvaluateRequest, EvaluateResponse


def scenario(*ids: str) -> dict[str, list[dict[str, str]]]:
    return {
        "selections": [
            {"measure_id": item}
            if item in {"M2", "M6", "M12", "M14"}
            else {"measure_id": item, "district_id": "saryarka" if item == "M5" else "nura"}
            for item in ids
        ]
    }


def test_health_is_available(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["X-Request-ID"]


def test_catalog_includes_exact_baseline_and_constraints(client: TestClient) -> None:
    response = client.get("/api/catalog")

    assert response.status_code == 200
    payload = response.json()
    assert payload["baseline"]["score"] == "52.55768"
    assert len(payload["catalog"]["measures"]) == 14
    assert len(payload["catalog"]["districts"]) == 5
    assert payload["catalog"]["budget"] == 100


def test_example_returns_exact_decimal_strings(client: TestClient) -> None:
    response = client.post("/api/scenarios/evaluate", json=scenario("M7", "M8", "M10", "M12", "M5"))

    assert response.status_code == 200
    result = response.json()["result"]
    assert isinstance(result["after"]["score"], str)
    assert Decimal(result["after"]["score"]) == Decimal("56.54307")
    assert result["spent"] == 95
    assert result["after"]["critical_count"] == 0
    assert len(result["district_changes"]) == 5
    assert len(result["changes"]) == 50


@pytest.mark.parametrize(
    "ids,code",
    [
        (("M7",), "selection_count"),
        (("M7", "M7", "M10", "M12", "M5"), "duplicate_measure"),
        (("M3", "M5", "M7", "M10", "M9"), "budget_exceeded"),
        (("M7", "M8", "M9", "M10", "M12"), "direction_limit"),
        (("M1", "M3", "M9", "M10", "M12"), "incompatible_measures"),
        (("wrong", "M8", "M10", "M12", "M5"), "unknown_measure"),
    ],
)
def test_invalid_domain_request_gets_422_without_score(
    client: TestClient,
    ids: tuple[str, ...],
    code: str,
) -> None:
    response = client.post("/api/scenarios/evaluate", json=scenario(*ids))

    assert response.status_code == 422
    assert response.json()["result"] is None
    assert code in {item["code"] for item in response.json()["issues"]}


@pytest.mark.parametrize(
    "choice,code",
    [
        ({"measure_id": "M7"}, "district_required"),
        ({"measure_id": "M7", "district_id": "wrong"}, "unknown_district"),
        ({"measure_id": "M12", "district_id": "nura"}, "unexpected_district"),
    ],
)
def test_district_rules_are_delegated_to_core(
    client: TestClient,
    choice: dict[str, str],
    code: str,
) -> None:
    payload = scenario("M7", "M8", "M10", "M12", "M5")
    index = 3 if choice["measure_id"] == "M12" else 0
    payload["selections"][index] = choice
    response = client.post("/api/scenarios/evaluate", json=payload)

    assert response.status_code == 422
    assert code in {item["code"] for item in response.json()["issues"]}


@pytest.mark.parametrize(
    "data",
    [
        '{"selections":[{"measure_id":7}]}',
        '{"selections":"wrong"}',
        '{"selections":[],"budget":100000}',
        '{"selections":[{"measure_id":"M7","cost":0}]}',
        "null",
        "not json",
        '{"selections":[{"measure_id":"M7","district_id":42}]}',
    ],
)
def test_malformed_payload_has_safe_structured_errors(client: TestClient, data: str) -> None:
    response = client.post(
        "/api/scenarios/evaluate", content=data, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    assert response.json()["result"] is None
    assert all(item["code"] == "invalid_input" for item in response.json()["issues"])
    assert all("location" in item for item in response.json()["issues"])
    assert "input" not in response.json()


def test_order_does_not_change_http_result(client: TestClient) -> None:
    first = scenario("M7", "M8", "M10", "M12", "M5")
    second = {"selections": list(reversed(first["selections"]))}

    assert (
        client.post("/api/scenarios/evaluate", json=first).json()
        == client.post("/api/scenarios/evaluate", json=second).json()
    )


def test_unexpected_error_hides_internal_details(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(request: EvaluateRequest) -> EvaluateResponse:
        raise RuntimeError("internal-secret-detail")

    monkeypatch.setattr(core_adapter, "evaluate", fail)
    response = client.post("/api/scenarios/evaluate", json=scenario("M7", "M8", "M10", "M12", "M5"))

    assert response.status_code == 500
    assert response.json()["issues"][0]["code"] == "internal_error"
    assert "internal-secret-detail" not in response.text
    assert response.headers["X-Request-ID"]


def test_openapi_documents_only_implemented_endpoints(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()

    assert set(schema["paths"]) == {
        "/api/health",
        "/api/catalog",
        "/api/scenarios/evaluate",
        "/api/scenarios/analyze",
    }
    assert "422" in schema["paths"]["/api/scenarios/evaluate"]["post"]["responses"]
    response = client.post("/api/scenarios/analyze", json=scenario("M7", "M8", "M10", "M12", "M5"))
    assert response.status_code == 200
    assert response.json()["status"] == "unavailable"
    assert response.json()["analysis"] is None
    assert "OPENAI_API_KEY" not in json.dumps(schema)
