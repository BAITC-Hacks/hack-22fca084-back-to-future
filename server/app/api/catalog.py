from fastapi import APIRouter

from ..core_adapter import read_catalog
from ..schemas import CatalogResponse

router = APIRouter(prefix="/api", tags=["catalog"])


@router.get(
    "/catalog", response_model=CatalogResponse, summary="Каталог и исходное состояние города"
)
def catalog() -> CatalogResponse:
    return read_catalog()
