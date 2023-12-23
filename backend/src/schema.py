from pydantic import BaseModel

class StoreSchema(BaseModel):
    name: str
    address: str
    longtitude: float
    latitude: float
