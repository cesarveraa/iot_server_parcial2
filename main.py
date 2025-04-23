from fastapi import FastAPI
from app.routers import nodes, readings, habitaciones

app = FastAPI(title="Sensor API v3", version="3.0")

app.include_router(habitaciones.router)
app.include_router(nodes.router)
app.include_router(readings.router)
