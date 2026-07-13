from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import get_claim_service
from app.api.schemas.claim_schemas import ClaimCreate, ClaimResponse
from app.services.claim_service import ClaimService

claims_router = APIRouter(tags=["Claims"])


@claims_router.post(
    "/api/cars/{car_id}/claims",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a claim for a car",
    description="Register a new insurance claim for an existing car.",
)
def create_claim(
    car_id: UUID,
    request: ClaimCreate,
    claim_service: ClaimService = Depends(get_claim_service),
):
    return claim_service.create_claim(
        car_id=car_id,
        request=request,
    )