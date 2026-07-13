from uuid import UUID

from pydantic import BaseModel, ConfigDict , Field , field_validator

from app.utils.enums.car_category import CarCategory


class CarOwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str


class CarWithOwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vin: str
    make: str | None
    model: str | None
    year_of_manufacture: int
    power: int
    cc: int
    category: CarCategory | None
    owner: CarOwnerResponse

class CarCreate(BaseModel):
    vin: str = Field(min_length=17, max_length=17)
    make: str = Field(min_length=2, max_length=150)
    model: str = Field(min_length=2, max_length=150)
    year_of_manufacture: int = Field(ge=1886, le=2100)
    category: CarCategory
    cc: int = Field(gt=0, lt=10000)
    power: int = Field(gt=0, lt=500)
    owner_id: UUID

    @field_validator("vin")
    @classmethod
    def validate_vin(cls, value: str) -> str:
        cleaned_value = value.strip().upper()

        if len(cleaned_value) != 17:
            raise ValueError("VIN must have exactly 17 characters")

        if not cleaned_value.isalnum():
            raise ValueError("VIN must contain only letters and numbers")

        return cleaned_value

    @field_validator("make", "model")
    @classmethod
    def validate_make_model(cls, value: str) -> str:
        cleaned_value = " ".join(value.strip().split())

        if len(cleaned_value) <= 1 or len(cleaned_value) > 150:
            raise ValueError("Value length must be between 2 and 150 characters")

        if not cleaned_value.replace(" ", "").isalnum():
            raise ValueError(
                "Value must contain only letters, numbers and single spaces between words"
            )

        return cleaned_value


class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vin: str
    make: str | None
    model: str | None
    year_of_manufacture: int
    category: CarCategory | None
    cc: int
    power: int
    owner_id: UUID