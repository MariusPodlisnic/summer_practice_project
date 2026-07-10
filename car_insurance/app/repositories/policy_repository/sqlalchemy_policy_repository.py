from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import InsurancePolicy


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