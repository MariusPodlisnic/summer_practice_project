from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import InsurancePolicy
from app.utils.enums.policy_status import PolicyStatus

class SqlAlchemyPolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_policy(self, policy: InsurancePolicy) -> InsurancePolicy:
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)

        return policy

    def get_overlapping_policy(
        self,
        car_id: UUID,
        start_date: date,
        end_date: date,
    ) -> InsurancePolicy | None:
        statement = select(InsurancePolicy).where(
            InsurancePolicy.car_id == car_id,
            start_date <= InsurancePolicy.end_date,
            end_date >= InsurancePolicy.start_date,
        )

        return self.db.scalar(statement)

    def has_valid_policy(
            self,
            car_id: UUID,
            check_date: date,
    ) -> bool:
        statement = select(InsurancePolicy).where(
            InsurancePolicy.car_id == car_id,
            InsurancePolicy.status == PolicyStatus.ACTIVE,
            InsurancePolicy.start_date <= check_date,
            InsurancePolicy.end_date >= check_date,
        )

        return self.db.scalar(statement) is not None

    def get_active_policy_by_car_id(
            self,
            car_id: UUID,
    ) -> InsurancePolicy | None:
        today = date.today()

        statement = select(InsurancePolicy).where(
            InsurancePolicy.car_id == car_id,
            InsurancePolicy.status == PolicyStatus.ACTIVE,
            InsurancePolicy.start_date <= today,
            InsurancePolicy.end_date >= today,
        )

        return self.db.scalar(statement)