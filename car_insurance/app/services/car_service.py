from uuid import UUID

from fastapi import HTTPException, status
from app.db.models import Car
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.repositories.car_repository.base import CarRepository
from app.repositories.owner_repository.base import OwnerRepository
from app.utils.enums.car_category import CarCategory
from app.api.schemas.car_history_schemas import (
    CarHistoryClaimResponse,
    CarHistoryPolicyResponse,
    CarHistoryResponse,
)
from app.api.schemas.car_schemas import CarCreate


class CarService:
    def __init__(
            self,
            repository: CarRepository,
            owner_repository: OwnerRepository,
    ):
        self.repository = repository
        self.owner_repository = owner_repository

    def get_categories(self) -> list[str]:
        return [category.value for category in CarCategory]

    def get_cars(
        self,
        page: int,
        per_page: int,
        make: str | None = None,
        model: str | None = None,
        category: list[CarCategory] | None = None,
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

    def get_car_history(
            self,
            car_id: UUID,
    ) -> CarHistoryResponse:
        car = self.repository.get_car_history(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        history_items = []

        for policy in car.policies:
            history_items.append(
                CarHistoryPolicyResponse(
                    type="POLICY",
                    policy_id=policy.id,
                    start_date=policy.start_date,
                    end_date=policy.end_date,
                    provider=policy.provider,
                    paid_amount=policy.paid_amount,
                    status=policy.status,
                )
            )

        for claim in car.claims:
            history_items.append(
                CarHistoryClaimResponse(
                    type="CLAIM",
                    claim_id=claim.id,
                    claim_date=claim.claim_date,
                    amount=claim.amount,
                    description=claim.description,
                )
            )

        history_items.sort(
            key=lambda item: item.start_date
            if isinstance(item, CarHistoryPolicyResponse)
            else item.claim_date
        )

        return history_items

    def create_car(
            self,
            request: CarCreate,
    ) -> Car:
        owner = self.owner_repository.get_by_id(request.owner_id)

        existing_car = self.repository.get_by_vin(request.vin)

        if existing_car is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Car with this VIN already exists",
            )

        car = Car(
            vin=request.vin,
            make=request.make,
            model=request.model,
            year_of_manufacture=request.year_of_manufacture,
            category=request.category,
            cc=request.cc,
            power=request.power,
            owner_id=request.owner_id,
        )

        return self.repository.create_car(car)

    def delete_car(
            self,
            car_id: UUID,
    ) -> None:
        car = self.repository.get_car_by_id(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        self.repository.delete_car(car)