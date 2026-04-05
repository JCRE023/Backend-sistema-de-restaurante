"""
CRUD para la entidad Factura.
Incluye operaciones básicas.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.Factura import Factura


def crear(
    db: Session,
    total: float,
    id_orden: UUID,
    id_usuario: UUID,
) -> Factura:
    """
    Crea una nueva factura inyectando la sesión 'db'.
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


def obtener_por_id(db: Session, id_factura: UUID) -> Optional[Factura]:
    """Obtiene una factura por su ID usando la sesión inyectada."""
    return db.query(Factura).filter(Factura.id_factura == id_factura).first()


def obtener_todos(db: Session) -> List[Factura]:
    """Obtiene todas las facturas de la base de datos."""
    return db.query(Factura).all()


def obtener_por_usuario(db: Session, id_usuario: UUID) -> List[Factura]:
    """Obtiene todas las facturas de un usuario específico."""
    return db.query(Factura).filter(Factura.id_usuario == id_usuario).all()


def actualizar(
    db: Session,
    id_factura: UUID,
    total: Optional[float] = None,
) -> Optional[Factura]:
    """Actualiza una factura existente."""
    # Importante: pasar 'db' a la función de búsqueda interna
    factura = obtener_por_id(db, id_factura)

    if not factura:
        return None

    if total is not None:
        factura.total = total

    db.commit()
    db.refresh(factura)
    return factura


def eliminar(db: Session, id_factura: UUID) -> bool:
    """Elimina una factura del sistema."""
    factura = obtener_por_id(db, id_factura)

    if not factura:
        return False

    db.delete(factura)
    db.commit()
    return True