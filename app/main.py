from pyexpat import model
from typing import Union
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# from . import crud, models, schemas
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/locations/{name}/{lat}/{lon}", response_model=schemas.Location)
def add_location(datos: schemas.Location, db: Session = Depends(get_db)):
    location = models.Location(name = datos.name, lat = datos.lat, lon = datos.lon)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@app.post("/temp/{temp}/{humidity}/{id_loc}", response_model=schemas.Temp)
def add_temp_humidity(datos: schemas.Temp, db: Session = Depends(get_db)):
    temperatura = models.Temp(temp = datos.temp, humidity = datos.humidity, location_id = datos.id_loc)
    db.add(temperatura)
    db.commit()
    db.refresh(temperatura)
    return temperatura

@app.get("/locations")
def max_temp(db: Session = Depends(get_db)):
   return db.query(models.Temp)

@app.get("/temp")
def get_locations(db: Session = Depends(get_db)):
   return db.query(models.Location)

# Método max_temp: devuelte el valor máximo de temperatura
@app.get("/temp/max_temp")
def max_temp(db: Session = Depends(get_db)):
   return db.query(models.Temp).order_by(-models.Temp.temp).first

# Método max_hum: devuelve el valor máximo de humedad
@app.get("/temp/max_hum")
def max_hum(db: Session = Depends(get_db)):
   return db.query(models.Temp).order_by(-models.Temp.humidity).first

# Método min_temp: devuelte el valor mínimo de temperatura
@app.get("/temp/min_temp")
def min_temp(db: Session = Depends(get_db)):
   return db.query(models.Temp).order_by(models.Temp.temp).first

# Método min_hum: devuelve el valor mínimo de humedad
@app.get("/temp/")
def min_hum(db: Session = Depends(get_db)):
   return db.query(models.Temp).order_by(models.Temp.humidity).first

# Método temp_max_by_qty: devuele la cantidad de registros de temperatura máximas solicitados
@app.get("/temp/temp_max_by_qty/{qty}")
def temp_max_by_qty(qty: int, db: Session = Depends(get_db)):
   return db.query(models.Temp).order_by(-models.Temp.temp).limit(qty)

# Método hum_max_by_qty: devuele la cantidad de registros de humedad máximas solicitados
@app.get("/temp/hum_max_by_qty/{qty}")
def hum_max_by_qty(qty: int, db: Session = Depends(get_db)):
   return db.query(models.Temp).order_by(-models.Temp.humidity).limit(qty)


# Método temp_min_by_qty: devuele la cantidad de registros de temperatura mínimas solicitados
@app.get("/temp/temp_min_by_qty/{qty}")
def temp_min_by_qty(qty: int, db: Session = Depends(get_db)):
   return db.query(models.Temp).order_by(models.Temp.temp).limit(qty)


# Método hum_min_by_qty: devuele la cantidad de registros de humedad mínimas solicitados
@app.get("/temp/hum_min_by_qty/{id_loc}")
def hum_min_by_qty(id_loc: int, db: Session = Depends(get_db)):
   return db.query(models.Temp).filter(models.Temp.location_id == id_loc).order_by(models.Temp.humidity).limit(10)


# Método temp_by_location: devuelve los últimos 10 registros de temperatura de la ubicación especificada
@app.get("/temp/temp_by_location/{id_loc}")
def temp_by_location(id_loc: int, db: Session = Depends(get_db)):
   return db.query(models.Temp).filter(models.Temp.location_id == id_loc).order_by(models.Temp.temp).limit(10)

# Método hum_by_location: devuelve los últimos 10 registros de humedad de la ubicación especificada