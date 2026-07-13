from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.utils.enums.policy_status import PolicyStatus


class PolicyCreate(BaseModel):
    provider: str | None = Field(default=None, min_length=1, max_length=100)
    start_date: date
    end_date: date
    paid_amount: Decimal = Field(gt=0, le=1_000_000)

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, value: str | None) -> str | None:
        if value is None:
            return value

        cleaned_value = " ".join(value.strip().split())

        if not cleaned_value.replace(" ", "").isalnum():
            raise ValueError(
                "Provider must contain only letters and numbers separated by single spaces"
            )

        return cleaned_value

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_year(cls, value: date) -> date:
        if value.year < 1900 or value.year > 2100:
            raise ValueError("Date year must be between 1900 and 2100")

        return value

    @model_validator(mode="after")
    def validate_date_order(self):
        if self.end_date < self.start_date:
            raise ValueError("endDate must be greater than or equal to startDate")

        return self


class PolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    car_id: UUID
    provider: str | None
    start_date: date
    end_date: date
    paid_amount: Decimal
    status: PolicyStatus

class InsuranceValidityResponse(BaseModel):
    car_id: UUID
    date: date
    valid: bool