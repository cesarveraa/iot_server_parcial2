from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
# ── NODO (asegúrate de que este modelo esté definido antes de Habitacion)
class Node(BaseModel):
    id: str
    nombre: str
    ubicacion: str
    habitacion_id: str
    temp_umbral: float
    co_umbral: int
    mix_ratio: float
    created_at: datetime

# ── HABITACIÓN
class HabitacionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class HabitacionCreate(HabitacionBase):
    pass

class Habitacion(HabitacionBase):
    id: str
    created_at: datetime = Field(..., description="Fecha de creación")
    nodos: List[Node] = Field(default_factory=list, description="Lista de nodos en esta habitación")

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
