import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import factura_crud
from src.entities.Orden import Orden
from src.entities.Usuario import Usuario


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
    """1. GET lista: Muestra todas las facturas emitidas."""
    return factura_crud.obtener_todos(db)


@router.get("/{id_factura}", response_model=FacturaRead)
def obtener_factura(db: DbSession, id_factura: UUID):
    """2. GET por id: Busca una factura en el historial."""
    f = factura_crud.obtener_por_id(db, id_factura)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
    return f


@router.post("", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def crear_factura(db: DbSession, data: FacturaCreate):
    """3. POST: Genera una nueva factura."""
    if data.total <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El total de la factura debe ser positivo",
        )
    orden = db.query(Orden).filter(Orden.id_orden == data.id_orden).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La orden especificada no existe",
        )
    usuario = db.query(Usuario).filter(Usuario.id_usuario == data.id_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario especificado no existe",
        )
    return factura_crud.crear(db, data.total, data.id_orden, data.id_usuario)


@router.put("/{id_factura}", response_model=FacturaRead)
def actualizar_factura(db: DbSession, id_factura: UUID, total: float):
    """4. PUT: Corrige el monto total de una factura existente."""
    f = factura_crud.actualizar(db, id_factura, total=total)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
    return f


@router.delete("/{id_factura}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(db: DbSession, id_factura: UUID):
    """5. DELETE: Elimina el registro de facturación."""
    if not factura_crud.eliminar(db, id_factura):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La factura no existe"
        )
    return None
