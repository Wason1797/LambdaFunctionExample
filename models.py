from db import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Float, Integer, DateTime


class Dweet(Base):
    __tablename__ = 'dweet'

    _id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)
    register_date = Column(DateTime, server_default=func.now())
