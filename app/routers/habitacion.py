from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas import Habitacion, HabitacionCreate
from .. import crud

router = APIRouter(prefix="/habitaciones", tags=["habitaciones"])

@router.post("/", response_model=Habitacion, status_code=201)
def create_hab(h: HabitacionCreate):
    return crud.create_habitacion(h.dict())

@router.get("/", response_model=List[Habitacion])
def read_habs():
    return crud.list_habitaciones()

@router.get("/{hab_id}", response_model=Habitacion)
def read_hab(hab_id: str):
    rec = crud.get_habitacion(hab_id)
    if not rec:
        raise HTTPException(404, "Habitación no encontrada")
    return rec

@router.put("/{hab_id}", response_model=Habitacion)
def update_hab(hab_id: str, h: HabitacionCreate):
    rec = crud.update_habitacion(hab_id, h.dict())
    if not rec:
        raise HTTPException(404, "Habitación no encontrada")
    return rec

@router.delete("/{hab_id}", status_code=204)
def delete_hab(hab_id: str):
    ok = crud.delete_habitacion(hab_id)
    if not ok:
        raise HTTPException(404, "Habitación no encontrada")
