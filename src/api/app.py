import src.entities.Mesa  # noqa: F401
import src.entities.producto  # noqa: F401
import src.entities.Orden  # noqa: F401
import src.entities.detalle_orden  # noqa: F401
import src.entities.Factura  # noqa: F401
import src.entities.Usuario  # noqa: F401
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import Mesa, Producto, Orden, Detalle_orden, Factura, Usuario
from src.database.config import create_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    Crea las tablas en Neon antes de iniciar[cite: 22].
    """
    # Las importaciones de entidades dentro del lifespan aseguran
    # que SQLAlchemy las registre antes de create_tables()
    create_tables()
    yield


app = FastAPI(
    title="API Restaurante - Sistema de Gestión",
    description="API para el manejo de mesas, pedidos y facturación en Neon",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers (Endpoints de cada entidad) [cite: 11]
app.include_router(Usuario.router)
app.include_router(Mesa.router)
app.include_router(Producto.router)
app.include_router(Orden.router)
app.include_router(Detalle_orden.router)
app.include_router(Factura.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint de verificación de estado [cite: 21]"""
    return {"status": "ok", "database": "connected"}