from pydantic import BaseModel, Field
from datetime import datetime

# ── NODO
class NodeBase(BaseModel):
    nombre: str
    ubicacion: str
    temp_umbral: float
    co_umbral: int
    mix_ratio: float

class NodeCreate(NodeBase):
    pass

class Node(NodeBase):
    id: str
    created_at: datetime

# ── LECTURA
class ReadingBase(BaseModel):
    temperatura_real: float
    temperatura_simulada: float
    temperatura_mixed: float
    humedad: float
    co_raw: int
    ventilador_on: bool

class ReadingCreate(ReadingBase):
    pass

class Reading(ReadingBase):
    id: str
    timestamp: datetime
