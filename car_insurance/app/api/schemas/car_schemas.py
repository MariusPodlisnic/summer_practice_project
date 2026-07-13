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
    vin: str = Field(min_length=1, max_length=50)
    make: str | None = Field(default=None, max_length=150)
    model: str | None = Field(default=None, max_length=150)
    year_of_manufacture: int = Field(ge=1886, le=2100)
    category: CarCategory | None = None
    cc: int = Field(gt=0, le=10000)
    power: int = Field(gt=0, le=5000)
    owner_id: UUID

    @field_validator("vin")
    @classmethod
    def validate_vin(cls, value: str) -> str:
        cleaned_value = value.strip().upper()

        if not cleaned_value.isalnum():
            raise ValueError("VIN must contain only letters and numbers")

        return cleaned_value

    @field_validator("make", "model")
    @classmethod
    def validate_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value

        cleaned_value = " ".join(value.strip().split())

        if not cleaned_value:
            return None

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