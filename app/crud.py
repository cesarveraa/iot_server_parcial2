from datetime import datetime
from google.cloud.firestore import Client, Query
from .database import db

# Colecciones
NODOS = db.collection("nodos")

# ── CRUD NODOS
def create_node(data: dict) -> dict:
    data["created_at"] = datetime.utcnow()
    doc = NODOS.document()
    doc.set(data)
    return {"id": doc.id, **data}

def get_node(node_id: str) -> dict:
    doc = NODOS.document(node_id).get()
    if not doc.exists:
        return None
    d = doc.to_dict()
    return {"id": doc.id, **d}

def list_nodes() -> list:
    docs = NODOS.order_by("created_at", direction=Query.DESCENDING).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def update_node(node_id: str, data: dict) -> dict:
    ref = NODOS.document(node_id)
    if not ref.get().exists:
        return None
    ref.update(data)
    d = ref.get().to_dict()
    return {"id": node_id, **d}

def delete_node(node_id: str) -> bool:
    ref = NODOS.document(node_id)
    if not ref.get().exists:
        return False
    ref.delete()
    return True

# ── CRUD LECTURAS
def create_reading(node_id: str, data: dict) -> dict:
    data["timestamp"] = datetime.utcnow()
    sub = NODOS.document(node_id).collection("lecturas").document()
    sub.set(data)
    return {"id": sub.id, **data}

def get_reading(node_id: str, reading_id: str) -> dict:
    ref = NODOS.document(node_id).collection("lecturas").document(reading_id)
    doc = ref.get()
    if not doc.exists:
        return None
    return {"id": doc.id, **doc.to_dict()}

def list_readings(node_id: str) -> list:
    coll = NODOS.document(node_id).collection("lecturas")
    docs = coll.order_by("timestamp", direction=Query.DESCENDING).stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

def update_reading(node_id: str, reading_id: str, data: dict) -> dict:
    ref = NODOS.document(node_id).collection("lecturas").document(reading_id)
    if not ref.get().exists:
        return None
    # no tocamos timestamp
    ref.update(data)
    doc = ref.get()
    return {"id": doc.id, **doc.to_dict()}

def delete_reading(node_id: str, reading_id: str) -> bool:
    ref = NODOS.document(node_id).collection("lecturas").document(reading_id)
    if not ref.get().exists:
        return False
    ref.delete()
    return True
