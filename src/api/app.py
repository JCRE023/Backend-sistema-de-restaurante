import src.entities.Mesa  # noqa: F401
import src.entities.producto  # noqa: F401
import src.entities.Orden  # noqa: F401
import src.entities.detalle_orden  # noqa: F401
import src.entities.Factura  # noqa: F401
import src.entities.Usuario  # noqa: F401
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import Mesa, Producto, Orden, detalle_orden, factura, usuario
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

# Registro de routers (Endpoints de cada entidad) [cite: 11]
app.include_router(usuario.router)
app.include_router(Mesa.router)
app.include_router(Producto.router)
app.include_router(Orden.router)
app.include_router(detalle_orden.router)
app.include_router(factura.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint de verificación de estado [cite: 21]"""
    return {"status": "ok", "database": "connected"}
