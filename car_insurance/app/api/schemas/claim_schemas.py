from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClaimCreate(BaseModel):
    claim_date: date
    description: str = Field(min_length=1, max_length=2000)
    amount: Decimal = Field(gt=0, le=1_000_000)

    @field_validator("claim_date")
    @classmethod
    def validate_claim_date(cls, value: date) -> date:
        if value.year < 1900 or value.year > 2100:
            raise ValueError("Claim date year must be between 1900 and 2100")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        cleaned_value = " ".join(value.strip().split())

        if not cleaned_value:
            raise ValueError("Description cannot be empty")

        return cleaned_value


class ClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    car_id: UUID
    claim_date: date
    description: str
    amount: Decimal