import json
from pathlib import Path

import pytest

from city_core import Selection
from city_core.serialization import parse_selections


@pytest.fixture
def example() -> tuple[Selection, ...]:
    return parse_selections(
        json.loads((Path(__file__).parent / "fixtures/example_95.json").read_text())
    )
