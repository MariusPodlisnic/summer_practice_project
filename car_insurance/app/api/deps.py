from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.car_repository.sqlalchemy_car_repository import (
    SqlAlchemyCarRepository,
)
from app.repositories.owner_repository.sqlalchemy_owner_repository import (
    SqlAlchemyOwnerRepository,
)
from app.repositories.policy_repository.sqlalchemy_policy_repository import (
    SqlAlchemyPolicyRepository,
)
from app.services.policy_service import PolicyService

from app.services.car_service import CarService
from app.services.owner_service import OwnerService


def get_car_service(
    db: Session = Depends(get_db),
) -> CarService:
    car_repository = SqlAlchemyCarRepository(db)
    return CarService(car_repository)


def get_owner_service(
    db: Session = Depends(get_db),
) -> OwnerService:
    owner_repository = SqlAlchemyOwnerRepository(db)
    return OwnerService(owner_repository)

def get_policy_service(
    db: Session = Depends(get_db),
) -> PolicyService:
    policy_repository = SqlAlchemyPolicyRepository(db)
    car_repository = SqlAlchemyCarRepository(db)

    return PolicyService(
        policy_repository=policy_repository,
        car_repository=car_repository,
    )