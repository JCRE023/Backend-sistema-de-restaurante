import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.entities.Factura import Factura
from src.crud import factura_crud


router = APIRouter(prefix="/facturas", tags=["Facturas"])


class FacturaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_factura: UUID
    total: float
    id_orden: UUID
    id_usuario: UUID
    fecha_creacion: Optional[datetime.datetime]


class FacturaCreate(BaseModel):
    total: float
    id_orden: UUID
    id_usuario: UUID


@router.get("", response_model=List[FacturaRead])
def listar_facturas(db: DbSession):
    """
    1. GET lista: Obtiene todas las facturas.
    """
    return db.query(Factura).all()


@router.get("/{id_factura}", response_model=FacturaRead)
def obtener_factura(db: DbSession, id_factura: UUID):
    """
    2. GET por id: Busca una factura por UUID.
    """
    factura = db.query(Factura).filter(Factura.id_factura == id_factura).first()

    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada",
        )

    return factura


@router.post("", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def crear_factura(db: DbSession, data: FacturaCreate):
    """
    3. POST: Crea una factura.
    """
    if data.total <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El total debe ser mayor a 0",
        )

    return factura_crud.crear(data.total, data.id_orden, data.id_usuario)


@router.put("/{id_factura}", response_model=FacturaRead)
def actualizar_factura(db: DbSession, id_factura: UUID, total: float):
    """
    4. PUT: Actualiza el total de una factura.
    """
    factura = factura_crud.actualizar(id_factura, total=total)

    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada",
        )

    return factura


@router.delete("/{id_factura}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(db: DbSession, id_factura: UUID):
    """
    5. DELETE: Elimina una factura.
    """
    factura = db.query(Factura).filter(Factura.id_factura == id_factura).first()

    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no existe",
        )

    db.delete(factura)
    db.commit()
    return None