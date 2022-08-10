from typing import List, Union

from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    lat: str
    lon: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True



class TempBase(BaseModel):
    temp: int
    humidity: int
    id: int
    ano: int
    mes: int
    dia: int
    hora: int

class TempCreate(TempBase):
    pass

class Temp(TempBase):
    # id: int
    location_id: int

    class Config:
        orm_mode = True

