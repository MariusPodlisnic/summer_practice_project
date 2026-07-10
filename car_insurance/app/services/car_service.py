from uuid import UUID

from app.api.schemas.pagination_schemas import PaginatedResponse
from app.repositories.car_repository.base import CarRepository
from app.utils.enums.car_category import CarCategory


class CarService:
    def __init__(self, repository: CarRepository):
        self.repository = repository

    def get_categories(self) -> list[str]:
        return [category.value for category in CarCategory]

    def get_cars(
        self,
        page: int,
        per_page: int,
        make: str | None = None,
        model: str | None = None,
        category: CarCategory | None = None,
        owner_id: UUID | None = None,
    ) -> PaginatedResponse:
        return self.repository.get_cars(
            page=page,
            per_page=per_page,
            make=make,
            model=model,
            category=category,
            owner_id=owner_id,
        )