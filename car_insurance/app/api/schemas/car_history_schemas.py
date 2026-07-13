from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from app.utils.enums.policy_status import PolicyStatus


class CarHistoryPolicyResponse(BaseModel):
    type: Literal["POLICY"]
    policy_id: UUID
    start_date: date
    end_date: date
    provider: str | None
    paid_amount: Decimal
    status: PolicyStatus


class CarHistoryClaimResponse(BaseModel):
    type: Literal["CLAIM"]
    claim_id: UUID
    claim_date: date
    amount: Decimal
    description: str


CarHistoryResponse = list[CarHistoryPolicyResponse | CarHistoryClaimResponse]