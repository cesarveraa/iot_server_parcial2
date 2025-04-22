from fastapi import FastAPI
from app.routers import nodes, readings

app = FastAPI(title="Sensor API v2", version="2.0")

app.include_router(nodes.router)
app.include_router(readings.router)
