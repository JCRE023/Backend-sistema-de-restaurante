from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.Mesa import Mesa

db = SessionLocal()


def crear_mesa(numero_mesa: str, id_usuario_creacion: UUID, estado: str) -> Mesa:

    mesa_limpia = numero_mesa.strip().upper()
    nombre_mesa = db.query(Mesa).filter(Mesa.numero_mesa == mesa_limpia).first()

    if nombre_mesa:
        raise ValueError("La Mesa ya existe")

    mesa = Mesa(
        numero_mesa=mesa_limpia,
        estado=estado.strip(),
        id_usuario_creacion=id_usuario_creacion,
    )

    db.add(mesa)
    db.commit()
    db.refresh(mesa)
    return mesa


def actualizar_estado(id_mesa: UUID, nuevo_estado: str) -> Optional[Mesa]:
    estado_mesas = ["DISPONIBLE", "OCUPADA", "RESERVADA"]

    mesa = obtener_por_id(id_mesa)

    if not mesa:
        return None

    estado_limpia = nuevo_estado.strip().upper()

    if estado_limpia not in estado_mesas:
        raise ValueError(
            f"El estado ingresado no es válido. "
            f"Los estados permitidos son: DISPONIBLE OCUPADA RESERVADA "
        )

    mesa.estado = estado_limpia

    db.commit()
    db.refresh(mesa)
    return mesa


def obtener_por_id(id_mesa: UUID) -> Optional[Mesa]:
    return db.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()


def obtener_todos() -> List[Mesa]:
    return db.query(Mesa).all()


def actualizar(
    id_mesa: UUID,
    id_usuario_edicion: UUID,
    **kwargs: dict,
) -> Optional[Mesa]:
    mesa = obtener_por_id(id_mesa)
    if not mesa:
        return None
    for key, value in kwargs.items():
        setattr(mesa, key, value)
    mesa.id_usuario_edicion = id_usuario_edicion
    db.commit()
    db.refresh(mesa)

    return mesa


def eliminar(id_mesa: UUID) -> bool:
    mesa = obtener_por_id(id_mesa)
    if not mesa:
        return False
    db.delete(mesa)
    db.commit()
    return True
