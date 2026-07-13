from datetime import date
from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi import HTTPException

from app.api.schemas.policy_schemas import PolicyCreate
from app.services.policy_service import PolicyService


def test_create_policy_success():
    policy_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = Mock()
    policy_repository.get_overlapping_policy.return_value = None
    policy_repository.create_policy.side_effect = lambda policy: policy

    service = PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )

    request = PolicyCreate(
        provider="Groupama",
        start_date="2031-01-01",
        end_date="2031-12-31",
        paid_amount=1200.00,
    )

    result = service.create_policy(
        car_id=car_id,
        request=request,
    )

    assert result.car_id == car_id
    assert result.provider == "Groupama"
    assert result.status.value == "ACTIVE"

    car_repository.get_car_by_id.assert_called_once_with(car_id)
    policy_repository.get_overlapping_policy.assert_called_once()
    policy_repository.create_policy.assert_called_once()


def test_create_policy_car_not_found():
    policy_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")
    car_repository.get_car_by_id.return_value = None

    service = PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )

    request = PolicyCreate(
        provider="Groupama",
        start_date="2031-01-01",
        end_date="2031-12-31",
        paid_amount=1200.00,
    )

    with pytest.raises(HTTPException) as exc:
        service.create_policy(car_id=car_id, request=request)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Car not found"

    policy_repository.create_policy.assert_not_called()


def test_create_policy_overlapping_policy():
    policy_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = Mock()
    policy_repository.get_overlapping_policy.return_value = Mock()

    service = PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )

    request = PolicyCreate(
        provider="Groupama",
        start_date="2031-01-01",
        end_date="2031-12-31",
        paid_amount=1200.00,
    )

    with pytest.raises(HTTPException) as exc:
        service.create_policy(car_id=car_id, request=request)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Policy overlaps with an existing policy for this car"

    policy_repository.create_policy.assert_not_called()


def test_check_insurance_validity_returns_true():
    policy_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = Mock()
    policy_repository.has_valid_policy.return_value = True

    service = PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )

    result = service.check_insurance_validity(
        car_id=car_id,
        check_date="2031-06-01",
    )

    assert result.car_id == car_id
    assert result.valid is True


def test_check_insurance_validity_car_not_found():
    policy_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = None

    service = PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )

    with pytest.raises(HTTPException) as exc:
        service.check_insurance_validity(
            car_id=car_id,
            check_date="2031-06-01",
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Car not found"

def test_check_insurance_validity_returns_true():
    policy_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = Mock()
    policy_repository.has_valid_policy.return_value = True

    service = PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )

    result = service.check_insurance_validity(
        car_id=car_id,
        check_date=date(2031, 6, 1),
    )

    assert result.car_id == car_id
    assert result.date == date(2031, 6, 1)
    assert result.valid is True

    car_repository.get_car_by_id.assert_called_once_with(car_id)
    policy_repository.has_valid_policy.assert_called_once_with(
        car_id=car_id,
        check_date=date(2031, 6, 1),
    )


def test_check_insurance_validity_car_not_found():
    policy_repository = Mock()
    car_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")

    car_repository.get_car_by_id.return_value = None

    service = PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )

    with pytest.raises(HTTPException) as exc:
        service.check_insurance_validity(
            car_id=car_id,
            check_date=date(2031, 6, 1),
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Car not found"

    car_repository.get_car_by_id.assert_called_once_with(car_id)
    policy_repository.has_valid_policy.assert_not_called()