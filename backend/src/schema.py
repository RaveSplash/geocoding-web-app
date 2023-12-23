from pydantic import BaseModel

class StoreSchema(BaseModel):
    id: int
    name: str
    address: str
    longtitude: float
    latitude: float
    state : str
