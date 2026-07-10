from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.api.schemas.pagination_schemas import PaginatedResponse
from app.db.models import Car
from app.utils.enums.car_category import CarCategory


class SqlAlchemyCarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cars(
        self,
        page: int,
        per_page: int,
        make: str | None = None,
        model: str | None = None,
        category: CarCategory | None = None,
        owner_id: UUID | None = None,
    ) -> PaginatedResponse:
        statement = select(Car).options(joinedload(Car.owner))
        count_statement = select(func.count()).select_from(Car)

        if make is not None:
            statement = statement.where(Car.make.ilike(f"%{make}%"))
            count_statement = count_statement.where(Car.make.ilike(f"%{make}%"))

        if model is not None:
            statement = statement.where(Car.model.ilike(f"%{model}%"))
            count_statement = count_statement.where(Car.model.ilike(f"%{model}%"))

        if category is not None:
            statement = statement.where(Car.category == category)
            count_statement = count_statement.where(Car.category == category)

        if owner_id is not None:
            statement = statement.where(Car.owner_id == owner_id)
            count_statement = count_statement.where(Car.owner_id == owner_id)

        offset = (page - 1) * per_page

        cars = list(
            self.db.scalars(
                statement.offset(offset).limit(per_page)
            ).all()
        )

        count = self.db.scalar(count_statement) or 0

        return PaginatedResponse(
            count=count,
            items=cars,
        )

    def get_car_by_id(self, car_id: UUID) -> Car | None:
        statement = (
            select(Car)
            .options(joinedload(Car.owner))
            .where(Car.id == car_id)
        )

        return self.db.scalar(statement)

    def create_car(self, request: Car) -> Car:
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)

        return request

    def get_by_vin(self, vin: str) -> Car | None:
        statement = select(Car).where(Car.vin == vin)

        return self.db.scalar(statement)

    def delete_car(self, car: Car) -> None:
        self.db.delete(car)
        self.db.commit()