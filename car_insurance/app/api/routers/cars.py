from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_car_service
from app.api.schemas.car_schemas import CarWithOwnerResponse
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.services.car_service import CarService
from app.utils.enums.car_category import CarCategory

cars_router = APIRouter(prefix="/api/cars", tags=["Cars"])


@cars_router.get(
    "",
    response_model=PaginatedResponse[CarWithOwnerResponse],
    summary="List cars with owners",
    description="Return all cars with their current owner information.",
)
def get_cars(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    make: str | None = None,
    model: str | None = None,
    category: list[CarCategory] | None = Query(default=None),
    owner_id: UUID | None = None,
    car_service: CarService = Depends(get_car_service),
):
    return car_service.get_cars(
        page=page,
        per_page=per_page,
        make=make,
        model=model,
        category=category,
        owner_id=owner_id,
    )


@cars_router.get(
    "/cars-categories",
    response_model=list[str],
    summary="Get car categories",
    description="Returns available car categories.",
)
def get_car_categories(
    car_service: CarService = Depends(get_car_service),
):
    return car_service.get_categories()