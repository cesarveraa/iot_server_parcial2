from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas import Reading, ReadingCreate
from .. import crud

router = APIRouter(prefix="/nodes/{node_id}/readings", tags=["readings"])

@router.post("/", response_model=Reading, status_code=201)
def create_reading(node_id: str, payload: ReadingCreate):
    if not crud.get_node(node_id):
        raise HTTPException(404, "Nodo no existe")
    return crud.create_reading(node_id, payload.dict())

@router.get("/", response_model=List[Reading])
def list_readings(node_id: str):
    if not crud.get_node(node_id):
        raise HTTPException(404, "Nodo no existe")
    return crud.list_readings(node_id)

@router.get("/{reading_id}", response_model=Reading)
def get_reading(node_id: str, reading_id: str):
    rec = crud.get_reading(node_id, reading_id)
    if not rec:
        raise HTTPException(404, "Lectura no encontrada")
    return rec

@router.put("/{reading_id}", response_model=Reading)
def update_reading(node_id: str, reading_id: str, payload: ReadingCreate):
    rec = crud.update_reading(node_id, reading_id, payload.dict())
    if not rec:
        raise HTTPException(404, "Lectura no encontrada")
    return rec

@router.delete("/{reading_id}", status_code=204)
def delete_reading(node_id: str, reading_id: str):
    ok = crud.delete_reading(node_id, reading_id)
    if not ok:
        raise HTTPException(404, "Lectura no encontrada")
