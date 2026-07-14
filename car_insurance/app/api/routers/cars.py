from uuid import UUID

from fastapi import APIRouter, Depends, Query , status

from app.api.deps import get_car_service
from app.api.schemas.car_schemas import (
    CarCreate,
    CarResponse,
    CarWithOwnerResponse,
)
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.api.schemas.car_history_schemas import CarHistoryResponse
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

@cars_router.post(
    "",
    response_model=CarResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create car",
    description="Create a new car for an existing owner.",
)
def create_car(
    request: CarCreate,
    car_service: CarService = Depends(get_car_service),
):
    return car_service.create_car(request)
@cars_router.get(
    "/{car_id}/history",
    response_model=CarHistoryResponse,
    summary="Get car history",
    description="Return car policy and claim history ordered chronologically.",
)
def get_car_history(
    car_id: UUID,
    car_service: CarService = Depends(get_car_service),
):
    return car_service.get_car_history(car_id)

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

@cars_router.get(
    "/{car_id}",
    response_model=CarWithOwnerResponse,
    summary="Get car by id",
    description="Return details about one car.",
)
def get_car_by_id(
    car_id: UUID,
    car_service: CarService = Depends(get_car_service),
):
    return car_service.get_car_by_id(car_id)
@cars_router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete car",
    description="Delete an existing car by id.",
)
def delete_car(
    car_id: UUID,
    car_service: CarService = Depends(get_car_service),
):
    car_service.delete_car(car_id)
