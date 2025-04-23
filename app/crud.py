from datetime import datetime
from google.cloud.firestore import Client, Query
from .database import db
from datetime import datetime
from google.cloud.firestore import Query

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
HABITACIONES = db.collection("habitaciones")


# ── Helper para nodos por habitación
def list_nodes_by_habitacion(hab_id: str) -> list:
    docs = NODOS.where("habitacion_id", "==", hab_id).stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

# ── CRUD HABITACIONES
def create_habitacion(data: dict) -> dict:
    data["created_at"] = datetime.utcnow()
    doc = HABITACIONES.document()
    doc.set(data)
    return {"id": doc.id, **data, "nodos": []}

def get_habitacion(hab_id: str) -> dict:
    doc = HABITACIONES.document(hab_id).get()
    if not doc.exists:
        return None
    d = doc.to_dict()
    hab = {
        "id": doc.id,
        **d,
        "nodos": list_nodes_by_habitacion(hab_id)
    }
    return hab

def list_habitaciones() -> list:
    docs = HABITACIONES.order_by("created_at", direction=Query.DESCENDING).stream()
    result = []
    for doc in docs:
        d = doc.to_dict()
        hab = {
            "id": doc.id,
            **d,
            "nodos": list_nodes_by_habitacion(doc.id)
        }
        result.append(hab)
    return result

def update_habitacion(hab_id: str, data: dict) -> dict:
    ref = HABITACIONES.document(hab_id)
    if not ref.get().exists:
        return None
    ref.update(data)
    d = ref.get().to_dict()
    return {
        "id": hab_id,
        **d,
        "nodos": list_nodes_by_habitacion(hab_id)
    }

def delete_habitacion(hab_id: str) -> bool:
    ref = HABITACIONES.document(hab_id)
    if not ref.get().exists:
        return False
    ref.delete()
    return True