from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.utils.enums.car_category import CarCategory
from app.utils.enums.policy_status import PolicyStatus


class CarHistoryOwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str | None


class CarHistoryPolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    provider: str | None
    start_date: date
    end_date: date
    paid_amount: Decimal
    status: PolicyStatus


class CarHistoryClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim_date: date
    description: str
    amount: Decimal


class CarHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vin: str
    make: str | None
    model: str | None
    year_of_manufacture: int
    category: CarCategory | None
    cc: int
    power: int
    owner: CarHistoryOwnerResponse
    policies: list[CarHistoryPolicyResponse]
    claims: list[CarHistoryClaimResponse]