from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.config import create_tables

# Importamos tus routers (los archivos que crearemos a continuación)
from . import Usuario, Mesa, Producto, Orden, Detalle_orden, Factura


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Registro de tus entidades para SQLAlchemy
    import src.entities.Mesa  # noqa: F401
    import src.entities.Usuario  # noqa: F401
    import src.entities.producto  # noqa: F401
    import src.entities.Orden  # noqa: F401
    import src.entities.detalle_orden  # noqa: F401

    # Crea las tablas en Neon al arrancar
    create_tables()
    yield


app = FastAPI(title="Restaurante API", version="1.0.0", lifespan=lifespan)

# Registro de los endpoints
app.include_router(usuario.router)
app.include_router(mesa.router)  # Tu entidad principal
app.include_router(producto.router)
app.include_router(pedido.router)  # Aquí va la lógica de Orden_crud
app.include_router(detalle_pedido.router)
app.include_router(pago.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
