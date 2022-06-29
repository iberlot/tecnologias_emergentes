from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base





class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    lat = Column(String(50))
    lon = Column(String(50))

    loca = relationship("Temp", back_populates="location")

    
class Temp(Base):
    __tablename__ = "temp"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    temp = Column(Integer)
    humidity = Column(Integer)
    location_id = Column(Integer, ForeignKey(Location.id))

    location = relationship("Location", back_populates="loca")