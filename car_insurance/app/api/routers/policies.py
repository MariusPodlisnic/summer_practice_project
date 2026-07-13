from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import get_policy_service
from app.api.schemas.policy_schemas import PolicyCreate, PolicyResponse
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