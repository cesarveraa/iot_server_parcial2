from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import nodes, readings, habitaciones

app = FastAPI(title="Sensor API v3", version="3.0")

# Define los orígenes permitidos
origins = [
    "*",
]

# Configura el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                      # Aquí especificas los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],                        # Puedes limitar a ["GET", "POST"] si prefieres
    allow_headers=["*"],
)

# Incluye tus routers
app.include_router(habitaciones.router)
app.include_router(nodes.router)
app.include_router(readings.router)
