from typing import Protocol
from uuid import UUID

from datetime import date
from app.db.models import InsurancePolicy


class PolicyRepository(Protocol):
    def create_policy(self, policy: InsurancePolicy) -> InsurancePolicy: ...

    def get_overlapping_policy(
        self,
        car_id: UUID,
        start_date,
        end_date,
    ) -> InsurancePolicy | None: ...

    def has_valid_policy(
            self,
            car_id: UUID,
            check_date: date,
    ) -> bool: ...

    def get_active_policy_by_car_id(
            self,
            car_id: UUID,
    ) -> InsurancePolicy | None: ...