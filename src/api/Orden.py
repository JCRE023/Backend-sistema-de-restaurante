import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud.Orden_crud import Orden_crud
from src.entities.Orden import Orden


router = APIRouter(prefix="/ordenes", tags=["Ordenes"])


class OrdenRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_orden: UUID
    id_mesa: UUID
    id_usuario: UUID
    estado: str
    fecha_registro: Optional[datetime.datetime]


@router.get("", response_model=List[OrdenRead])
def listar_ordenes(db: DbSession):
    """
    1. GET lista: Obtiene todas las órdenes registradas[cite: 12].
    """
    return db.query(Orden).all()


@router.get("/{id_orden}", response_model=OrdenRead)
def obtener_orden(db: DbSession, id_orden: UUID):
    """
    2. GET por id: Busca una orden específica por su UUID[cite: 13].
    """
    orden = db.query(Orden).filter(Orden.id_orden == id_orden).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
        )
    return orden


@router.post("/abrir", response_model=OrdenRead, status_code=status.HTTP_201_CREATED)
def abrir_orden(db: DbSession, id_mesa: UUID, id_usuario: UUID):
    """
    3. POST: Crea una nueva orden y actualiza el estado de la mesa[cite: 14].
    """
    try:
        crud = Orden_crud(db)
        return crud.crear_orden(id_mesa, id_usuario)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_orden}/cerrar", response_model=OrdenRead)
def cerrar_orden(db: DbSession, id_orden: UUID):
    """
    4. PUT: Edita el estado de la orden a 'CERRADA'[cite: 15].
    """
    crud = Orden_crud(db)
    orden_actualizada = crud.cerrar_orden(id_orden)
    if not orden_actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo cerrar la orden o no existe",
        )
    return orden_actualizada


@router.delete("/{id_orden}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden(db: DbSession, id_orden: UUID):
    """
    5. DELETE: Elimina físicamente el registro de la orden[cite: 16].
    """
    orden = db.query(Orden).filter(Orden.id_orden == id_orden).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La orden no existe"
        )
    db.delete(orden)
    db.commit()
    return None
