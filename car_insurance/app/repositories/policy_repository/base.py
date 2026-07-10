from typing import Protocol
from uuid import UUID

from app.db.models import InsurancePolicy


class PolicyRepository(Protocol):
    def create_policy(self, policy: InsurancePolicy) -> InsurancePolicy: ...

    def get_overlapping_policy(
        self,
        car_id: UUID,
        start_date,
        end_date,
    ) -> InsurancePolicy | None: ...