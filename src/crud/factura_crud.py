"""
CRUD para la entidad Factura.
Incluye operaciones básicas.
"""

from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.Factura import Factura

db = SessionLocal()


def crear(
    total: float,
    id_orden: UUID,
    id_usuario: UUID,
) -> Factura:
    """
    Crea una nueva factura.


    """

    factura = Factura(
        total=total,
        id_orden=id_orden,
        id_usuario=id_usuario,
    )

    db.add(factura)
    db.commit()
    db.refresh(factura)

    return factura


def obtener_por_id(id_factura: UUID) -> Optional[Factura]:
    """
    Obtiene una factura por su ID.


    """

    return db.query(Factura).filter(Factura.id_factura == id_factura).first()


def obtener_todos() -> List[Factura]:
    """
    Obtiene todas las facturas.

    """

    return db.query(Factura).all()


def obtener_por_usuario(id_usuario: UUID) -> List[Factura]:
    """
    Obtiene todas las facturas de un usuario.

    """

    return db.query(Factura).filter(Factura.id_usuario == id_usuario).all()


def actualizar(
    id_factura: UUID,
    *,
    total: Optional[float] = None,
) -> Optional[Factura]:
    """
    Actualiza una factura.

    """

    factura = obtener_por_id(id_factura)

    if not factura:
        return None

    if total is not None:
        factura.total = total

    db.commit()
    db.refresh(factura)

    return factura


def eliminar(id_factura: UUID) -> bool:
    """
    Elimina una factura.

    """

    factura = obtener_por_id(id_factura)

    if not factura:
        return False

    db.delete(factura)
    db.commit()

    return True
