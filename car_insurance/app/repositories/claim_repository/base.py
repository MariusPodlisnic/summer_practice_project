from typing import Protocol

from app.db.models import Claim


class ClaimRepository(Protocol):
    def create_claim(self, claim: Claim) -> Claim: ...