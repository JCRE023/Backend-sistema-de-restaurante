import sys
from typing import Optional
from uuid import UUID


from src.crud import Detalle_orden_crud as crud_Detalle_orden
from src.crud import Orden_crud as crud_Orden
from src.crud import Producto_crud as crud_Producto
from src.crud import Mesa_crud as crud_Mesa
from src.entities.usuario import Usuario


from src.database.config import create_tables

import os
from dotenv import load_dotenv

# Cargar .env desde la carpeta del proyecto (donde está init_db.py)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from sqlalchemy.exc import OperationalError
import src.entities.Orden  # noqa: F401 - registrar modelo
import src.entities.detalle_orden  # noqa: F401 - registrar modelo
import src.entities.Usuario  # noqa: F401 - registrar modelo
import src.entities.producto  # noqa: F401 - registrar modelo
import src.entities.Factura  # noqa: F401 - registrar modelo
import src.entities.Mesa  # noqa: F401 - registrar modelo
from src.database.config import create_tables

if __name__ == "__main__":
    try:
        create_tables()
        print("Tablas creadas correctamente en Neon.")
    except OperationalError as e:
        if "password authentication failed" in str(e).lower():
            print("Error: Neon rechazó la contraseña (password authentication failed).")
            print(
                "  - Entra a https://console.neon.tech y revisa la conexión del proyecto."
            )
            print(
                "  - Copia de nuevo la connection string (Connection string) y actualiza .env."
            )
            print(
                "  - Si la contraseña tiene caracteres especiales (& # @ ?), codifícala en URL"
            )
        else:
            print("Error de conexión a la base de datos:", e)
        raise SystemExit(1)
