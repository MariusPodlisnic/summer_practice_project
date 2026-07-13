from sqlalchemy.orm import Session

from app.db.models import Claim
from app.repositories.claim_repository.base import ClaimRepository


class SqlAlchemyClaimRepository(ClaimRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_claim(self, claim: Claim) -> Claim:
        self.db.add(claim)
        self.db.commit()
        self.db.refresh(claim)

        return claim