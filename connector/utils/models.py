from pydantic import BaseModel
from typing import Optional

class IncrementalLoadRequest(BaseModel):
    # Añade los campos necesarios según tu lógica
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class BackfillRequest(BaseModel):
    # Añade los campos necesarios según tu lógica
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class WeatherData(BaseModel):
    fecha: str
    indicativo: str
    nombre: str
    provincia: str
    altitud: float
    tmed: Optional[float] = None
    prec: Optional[float] = None
    tmin: Optional[float] = None
    horatmin: Optional[str] = None
    tmax: Optional[float] = None
    horatmax: Optional[str] = None
    dir: Optional[float] = None
    velmedia: Optional[float] = None
    racha: Optional[float] = None
    horaracha: Optional[str] = None
    sol: Optional[float] = None
    presmax: Optional[float] = None
    horapresmax: Optional[str] = None
    presmin: Optional[float] = None
    horapresmin: Optional[str] = None
    hrmedia: Optional[float] = None
    hrmax: Optional[float] = None
    horahrmax: Optional[str] = None
    hrmin: Optional[float] = None
    horahrmin: Optional[str] = None

class Estacion(BaseModel):
    latitud: float
    longitud: float
    provincia: str
    indicativo: str
    altitud: float
    nombre: str
    indsinop: str
