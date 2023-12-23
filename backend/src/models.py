
from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, unique=True)
    longtitude = Column(Double, nullable=True)
    latitude = Column(Double, nullable=True)
    state= Column(String)
