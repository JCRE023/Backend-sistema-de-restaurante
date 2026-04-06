"""
Script para crear las tablas en la base de datos.
"""

from src.database.config import engine, Base

# Importar todas las entidades para que SQLAlchemy las registre
from src.entities.Usuario import Usuario  # noqa: F401
from src.entities.Factura import Factura  # noqa: F401
from src.entities.Orden import Orden  # noqa: F401
from src.entities.Mesa import Mesa  # noqa: F401
from src.entities.producto import Producto  # noqa: F401
from src.entities.detalle_orden import Detalle_orden  # noqa: F401


def init_db() -> None:
    """Crea todas las tablas en la base de datos."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Tabla creadas correctamente")
