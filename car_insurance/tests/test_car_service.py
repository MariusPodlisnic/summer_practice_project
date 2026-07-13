from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi import HTTPException

from app.api.schemas.car_schemas import CarCreate
from app.services.car_service import CarService


def test_create_car_success():
    car_repository = Mock()
    owner_repository = Mock()

    owner_id = UUID("11111111-1111-1111-1111-111111111111")

    owner_repository.get_by_id.return_value = Mock()
    car_repository.get_by_vin.return_value = None
    car_repository.create_car.side_effect = lambda car: car

    service = CarService(
        repository=car_repository,
        owner_repository=owner_repository,
    )

    request = CarCreate(
        vin="WAUZZZ8V5KA000123",
        make="Audi",
        model="A3",
        year_of_manufacture=2020,
        category="EURO6",
        cc=1600,
        power=150,
        owner_id=owner_id,
    )

    result = service.create_car(request)

    assert result.vin == "WAUZZZ8V5KA000123"
    assert result.make == "Audi"
    assert result.model == "A3"
    assert result.owner_id == owner_id

    owner_repository.get_by_id.assert_called_once_with(owner_id)
    car_repository.get_by_vin.assert_called_once_with("WAUZZZ8V5KA000123")
    car_repository.create_car.assert_called_once()


def test_create_car_duplicate_vin():
    car_repository = Mock()
    owner_repository = Mock()

    owner_id = UUID("11111111-1111-1111-1111-111111111111")

    owner_repository.get_by_id.return_value = Mock()
    car_repository.get_by_vin.return_value = Mock()

    service = CarService(
        repository=car_repository,
        owner_repository=owner_repository,
    )

    request = CarCreate(
        vin="WAUZZZ8V5KA000123",
        make="Audi",
        model="A3",
        year_of_manufacture=2020,
        category="EURO6",
        cc=1600,
        power=150,
        owner_id=owner_id,
    )

    with pytest.raises(HTTPException) as exc:
        service.create_car(request)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Car with this VIN already exists"

    car_repository.create_car.assert_not_called()


def test_get_car_history_car_not_found():
    car_repository = Mock()
    owner_repository = Mock()

    car_id = UUID("33333333-3333-3333-3333-333333333333")
    car_repository.get_car_history.return_value = None

    service = CarService(
        repository=car_repository,
        owner_repository=owner_repository,
    )

    with pytest.raises(HTTPException) as exc:
        service.get_car_history(car_id)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Car not found"