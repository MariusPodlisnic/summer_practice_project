from uuid import UUID

from fastapi import HTTPException, status

from app.api.schemas.claim_schemas import ClaimCreate
from app.db.models import Claim
from app.repositories.car_repository.base import CarRepository
from app.repositories.claim_repository.base import ClaimRepository


class ClaimService:
    def __init__(
        self,
        claim_repository: ClaimRepository,
        car_repository: CarRepository,
    ):
        self.claim_repository = claim_repository
        self.car_repository = car_repository

    def create_claim(
        self,
        car_id: UUID,
        request: ClaimCreate,
    ) -> Claim:
        car = self.car_repository.get_car_by_id(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        claim = Claim(
            car_id=car_id,
            claim_date=request.claim_date,
            description=request.description,
            amount=request.amount,
        )

        return self.claim_repository.create_claim(claim)