import pytest
from pydantic import ValidationError

from app.api.schemas.car_schemas import CarCreate


def test_car_create_accepts_valid_data():
    car = CarCreate(
        vin="WAUZZZ8V5KA000123",
        make="Audi",
        model="A3",
        year_of_manufacture=2020,
        category="EURO6",
        cc=1600,
        power=150,
        owner_id="11111111-1111-1111-1111-111111111111",
    )

    assert car.vin == "WAUZZZ8V5KA000123"
    assert car.make == "Audi"
    assert car.model == "A3"
    assert car.year_of_manufacture == 2020
    assert car.category.value == "EURO6"
    assert car.cc == 1600
    assert car.power == 150


def test_car_create_rejects_short_vin():
    with pytest.raises(ValidationError):
        CarCreate(
            vin="ABC",
            make="Audi",
            model="A3",
            year_of_manufacture=2020,
            category="EURO6",
            cc=1600,
            power=150,
            owner_id="11111111-1111-1111-1111-111111111111",
        )


def test_car_create_rejects_non_alphanumeric_vin():
    with pytest.raises(ValidationError):
        CarCreate(
            vin="WAUZZZ8V5KA000-12",
            make="Audi",
            model="A3",
            year_of_manufacture=2020,
            category="EURO6",
            cc=1600,
            power=150,
            owner_id="11111111-1111-1111-1111-111111111111",
        )


def test_car_create_rejects_invalid_category():
    with pytest.raises(ValidationError):
        CarCreate(
            vin="WAUZZZ8V5KA000123",
            make="Audi",
            model="A3",
            year_of_manufacture=2020,
            category="B",
            cc=1600,
            power=150,
            owner_id="11111111-1111-1111-1111-111111111111",
        )


def test_car_create_rejects_cc_equal_to_10000():
    with pytest.raises(ValidationError):
        CarCreate(
            vin="WAUZZZ8V5KA000123",
            make="Audi",
            model="A3",
            year_of_manufacture=2020,
            category="EURO6",
            cc=10000,
            power=150,
            owner_id="11111111-1111-1111-1111-111111111111",
        )


def test_car_create_rejects_power_equal_to_500():
    with pytest.raises(ValidationError):
        CarCreate(
            vin="WAUZZZ8V5KA000123",
            make="Audi",
            model="A3",
            year_of_manufacture=2020,
            category="EURO6",
            cc=1600,
            power=500,
            owner_id="11111111-1111-1111-1111-111111111111",
        )


def test_car_create_rejects_invalid_make_characters():
    with pytest.raises(ValidationError):
        CarCreate(
            vin="WAUZZZ8V5KA000123",
            make="Audi!",
            model="A3",
            year_of_manufacture=2020,
            category="EURO6",
            cc=1600,
            power=150,
            owner_id="11111111-1111-1111-1111-111111111111",
        )


def test_car_create_normalizes_multiple_spaces_in_make():
    car = CarCreate(
        vin="WAUZZZ8V5KA000123",
        make="Audi     Sport",
        model="A3",
        year_of_manufacture=2020,
        category="EURO6",
        cc=1600,
        power=150,
        owner_id="11111111-1111-1111-1111-111111111111",
    )

    assert car.make == "Audi Sport"