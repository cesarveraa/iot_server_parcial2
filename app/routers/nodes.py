from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas import Node, NodeCreate
from .. import crud

router = APIRouter(prefix="/nodes", tags=["nodes"])

@router.post("/", response_model=Node, status_code=201)
def create_node(payload: NodeCreate):
    rec = crud.create_node(payload.dict())
    return rec

@router.get("/", response_model=List[Node])
def list_nodes():
    return crud.list_nodes()

@router.get("/{node_id}", response_model=Node)
def get_node(node_id: str):
    rec = crud.get_node(node_id)
    if not rec:
        raise HTTPException(404, "Nodo no encontrado")
    return rec

@router.put("/{node_id}", response_model=Node)
def update_node(node_id: str, payload: NodeCreate):
    rec = crud.update_node(node_id, payload.dict())
    if not rec:
        raise HTTPException(404, "Nodo no encontrado")
    return rec

@router.delete("/{node_id}", status_code=204)
def delete_node(node_id: str):
    ok = crud.delete_node(node_id)
    if not ok:
        raise HTTPException(404, "Nodo no encontrado")
