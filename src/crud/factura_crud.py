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

    Parameters
    ----------
    total : float
        Valor total de la factura.
    id_orden : UUID
        Identificador de la orden.
    id_usuario : UUID
        Identificador del usuario.

    Returns
    -------
    Factura
        Factura creada.
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

    Parameters
    ----------
    id_factura : UUID
        Identificador de la factura.

    Returns
    -------
    Optional[Factura]
        Factura encontrada o None.
    """

    return db.query(Factura).filter(
        Factura.id_factura == id_factura
    ).first()


def obtener_todos() -> List[Factura]:
    """
    Obtiene todas las facturas.

    Returns
    -------
    List[Factura]
        Lista de facturas.
    """

    return db.query(Factura).all()


def obtener_por_usuario(id_usuario: UUID) -> List[Factura]:
    """
    Obtiene todas las facturas de un usuario.

    Parameters
    ----------
    id_usuario : UUID
        Identificador del usuario.

    Returns
    -------
    List[Factura]
        Lista de facturas del usuario.
    """

    return db.query(Factura).filter(
        Factura.id_usuario == id_usuario
    ).all()


def actualizar(
    id_factura: UUID,
    *,
    total: Optional[float] = None,
) -> Optional[Factura]:
    """
    Actualiza una factura.

    Parameters
    ----------
    id_factura : UUID
        Identificador de la factura.
    total : float, optional
        Nuevo valor total.

    Returns
    -------
    Optional[Factura]
        Factura actualizada o None si no existe.
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

    Parameters
    ----------
    id_factura : UUID
        Identificador de la factura.

    Returns
    -------
    bool
        True si se eliminó, False si no existe.
    """

    factura = obtener_por_id(id_factura)

    if not factura:
        return False

    db.delete(factura)
    db.commit()

    return True