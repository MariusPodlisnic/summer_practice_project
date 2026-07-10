from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.api.schemas.owner_schemas import OwnerResponse
from app.utils.enums.car_category import CarCategory

class CarOwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:UUID
    name:str
    email:str

class CarWithOwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vin: str
    make: str | None
    model: str | None
    year_of_manufacture: int
    power: int
    cc: int
    category: CarCategory | None
    owner: OwnerResponse