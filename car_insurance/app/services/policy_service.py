from uuid import UUID
from datetime import date
from fastapi import HTTPException, status

from app.api.schemas.policy_schemas import InsuranceValidityResponse, PolicyCreate
from app.db.models import InsurancePolicy
from app.repositories.car_repository.base import CarRepository
from app.repositories.policy_repository.base import PolicyRepository
from app.utils.enums.policy_status import PolicyStatus


class PolicyService:
    def __init__(
        self,
        policy_repository: PolicyRepository,
        car_repository: CarRepository,
    ):
        self.policy_repository = policy_repository
        self.car_repository = car_repository

    def create_policy(
        self,
        car_id: UUID,
        request: PolicyCreate,
    ) -> InsurancePolicy:
        car = self.car_repository.get_car_by_id(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        overlapping_policy = self.policy_repository.get_overlapping_policy(
            car_id=car_id,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        if overlapping_policy is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Policy overlaps with an existing policy for this car",
            )

        policy = InsurancePolicy(
            car_id=car_id,
            provider=request.provider,
            start_date=request.start_date,
            end_date=request.end_date,
            paid_amount=request.paid_amount,
            status=PolicyStatus.ACTIVE,
        )

        return self.policy_repository.create_policy(policy)

    def get_active_policy(
            self,
            car_id: UUID,
    ) -> InsurancePolicy:
        car = self.car_repository.get_car_by_id(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        active_policy = self.policy_repository.get_active_policy_by_car_id(car_id)

        if active_policy is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active policy not found",
            )

        return active_policy
    
    def check_insurance_validity(
            self,
            car_id: UUID,
            check_date: date,
    ) -> InsuranceValidityResponse:
        car = self.car_repository.get_car_by_id(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        is_valid = self.policy_repository.has_valid_policy(
            car_id=car_id,
            check_date=check_date,
        )

        return InsuranceValidityResponse(
            car_id=car_id,
            date=check_date,
            valid=is_valid,
        )