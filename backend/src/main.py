# functions
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import json
from .utils import get_coordinates, scrap_by_state


# structures
from sqlalchemy import String
from sqlalchemy.orm import Session
from .schema import StoreSchema
from .database import SessionLocal
from .models import Store
from typing import List

app = FastAPI()

# CORS settings
origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    "/stores/{state}",
    response_model=List[StoreSchema],
    tags=["Store"],
    name="Populate Store",
)
def create_store(state: str, db: Session = Depends(get_db)):
    """
    Populate Store - this api will take a state in Malaysia and populate it in the database for future perusal.
    """
    db_stores = []
    stores = json.loads(scrap_by_state(state))
    for store in stores:
        print(store)
        # check if the store address already exist
        existing_store = (
            db.query(Store).filter(Store.address == store["address"]).first()
        )
        if existing_store:
            print("this address already exist")
        else:
            db_store = Store(**store)
            # use my function to get coordinates
            (longtitude, latitude) = get_coordinates(store["address"])
            db_store.longtitude = longtitude
            db_store.latitude = latitude
            db_store.state = state
            db.add(db_store)
            db_stores.append(db_store)
    db.commit()

    # Refresh each individual store
    for db_store in db_stores:
        db.refresh(db_store)
    return db_stores


@app.get("/stores", response_model=List[StoreSchema], tags=["Store"], name="Get Stores")
def get_store(db: Session = Depends(get_db)):
    """
    Get Store - this api will retrieve all stores from the db with it's details
    """
    stores = db.query(Store).all()
    return stores
