from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_coordinates

from .schema import StoreSchema
from .database import SessionLocal
from .models import Store

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/stores/", response_model=list[StoreSchema] ,tags=["Store"],name="Populate Store")
def create_store(stores: list[StoreSchema], db: Session = Depends(get_db)):
    """
    Populate Store - this api will take an array of store object and populate it in the database for future perusal.
    """
    db_stores = []
    base_url = "https://www.openstreetmap.org/search?query="
    for store in stores:
        #check if the store address already exist
        existing_store = db.query(Store).filter(Store.address == store.address).first()
        if existing_store:
            print("this address already exist")
        else:
            db_store = Store(**store.model_dump())
            # use my function to get coordinates 
            (longtitude, latitude) = get_coordinates(store.address)
            db_store.longtitude = longtitude
            db_store.latitude = latitude
            db.add(db_store)
            db_stores.append(db_store)
    db.commit()

   # Refresh each individual store
    for db_store in db_stores:
        db.refresh(db_store)
    return db_stores