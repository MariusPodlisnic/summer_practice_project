from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_policy_service
from app.api.schemas.policy_schemas import PolicyCreate, PolicyResponse , InsuranceValidityResponse
from app.services.policy_service import PolicyService

policies_router = APIRouter(tags=["Policies"])


@policies_router.post(
    "/api/cars/{car_id}/policies",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create insurance policy for car",
    description="Create a new insurance policy for an existing car.",
)
def create_policy(
    car_id: UUID,
    request: PolicyCreate,
    policy_service: PolicyService = Depends(get_policy_service),
):
    return policy_service.create_policy(
        car_id=car_id,
        request=request,
    )

@policies_router.get(
    "/api/policies/active-policy",
    response_model=PolicyResponse,
    summary="Get active policy for car",
    description="Return the currently active policy for a car.",
)
def get_active_policy(
    car_id: UUID = Query(...),
    policy_service: PolicyService = Depends(get_policy_service),
):
    return policy_service.get_active_policy(car_id)
@policies_router.get(
    "/api/cars/{car_id}/insurance-valid",
    response_model=InsuranceValidityResponse,
    summary="Check insurance validity",
    description="Check if a car has valid insurance on a specific date.",
)
def check_insurance_validity(
    car_id: UUID,
    date: date = Query(...),
    policy_service: PolicyService = Depends(get_policy_service),
):
    return policy_service.check_insurance_validity(
        car_id=car_id,
        check_date=date,
    )