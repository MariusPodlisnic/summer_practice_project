from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi import HTTPException

from app.api.schemas.claim_schemas import ClaimCreate
from app.db.models import Car, Claim
from app.services.claim_service import ClaimService


def test_create_claim_success():
    claim_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = Car(id=car_id)

    claim_repository.create_claim.side_effect = lambda claim: claim

    service = ClaimService(
        claim_repository=claim_repository,
        car_repository=car_repository,
    )

    request = ClaimCreate(
        claim_date="2025-06-10",
        description="Front bumper damage",
        amount=750.00,
    )

    result = service.create_claim(
        car_id=car_id,
        request=request,
    )

    assert isinstance(result, Claim)
    assert result.car_id == car_id
    assert result.description == "Front bumper damage"
    assert result.amount == 750.00

    car_repository.get_car_by_id.assert_called_once_with(car_id)
    claim_repository.create_claim.assert_called_once()


def test_create_claim_car_not_found():
    claim_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = None

    service = ClaimService(
        claim_repository=claim_repository,
        car_repository=car_repository,
    )

    request = ClaimCreate(
        claim_date="2025-06-10",
        description="Front bumper damage",
        amount=750.00,
    )

    with pytest.raises(HTTPException) as exc:
        service.create_claim(
            car_id=car_id,
            request=request,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Car not found"

    car_repository.get_car_by_id.assert_called_once_with(car_id)
    claim_repository.create_claim.assert_not_called()