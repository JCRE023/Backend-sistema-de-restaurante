import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud.Detalle_orden_crud import Detalle_orden_crud

router = APIRouter(prefix="/detalles-orden", tags=["Detalle de Orden"])


class DetalleBase(BaseModel):
    id_orden: UUID
    id_producto: UUID
    cantidad: int


class DetalleCreate(DetalleBase):
    """Esquema para crear un nuevo item en la orden."""

    pass


class DetalleUpdate(BaseModel):
    """Esquema para actualizar solo la cantidad."""

    cantidad: int


class DetalleRead(DetalleBase):
    """Esquema para mostrar la información al cliente."""

    model_config = ConfigDict(from_attributes=True)
    id_detalle: UUID


@router.post("/", response_model=DetalleRead, status_code=status.HTTP_201_CREATED)
def agregar_item_a_orden(data: DetalleCreate, db: DbSession):
    """
    Agrega un producto a una orden.
    Lanza error 400 si la orden está cerrada o la cantidad es <= 0.
    """
    crud = Detalle_orden_crud(db)
    try:
        return crud.crear_detalle(
            id_orden=data.id_orden, id_producto=data.id_producto, cantidad=data.cantidad
        )
    except ValueError as e:
        # Aquí atrapamos las validaciones de negocio que hiciste en el CRUD
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/orden/{id_orden}", response_model=List[DetalleRead])
def listar_detalles_por_orden(id_orden: UUID, db: DbSession):
    """Obtiene todos los productos de una orden específica."""
    crud = Detalle_orden_crud(db)
    return crud.obtener_detalles_por_orden(id_orden)


@router.get("/{id_detalle}", response_model=DetalleRead)
def obtener_detalle_especifico(id_detalle: UUID, db: DbSession):
    """Busca un registro de detalle por su ID único."""
    crud = Detalle_orden_crud(db)
    detalle = crud.obtener_detalle(id_detalle)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.put("/{id_detalle}", response_model=DetalleRead)
def modificar_cantidad_detalle(id_detalle: UUID, data: DetalleUpdate, db: DbSession):
    """
    Actualiza la cantidad de un producto ya pedido.
    Solo funciona si la orden sigue abierta.
    """
    crud = Detalle_orden_crud(db)
    try:
        detalle = crud.actualizar_detalle(id_detalle, data.cantidad)
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return detalle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id_detalle}", status_code=status.HTTP_204_NO_CONTENT)
def quitar_item_de_orden(id_detalle: UUID, db: DbSession):
    """Elimina un producto de la orden."""
    crud = Detalle_orden_crud(db)
    try:
        if not crud.eliminar_detalle(id_detalle):
            raise HTTPException(status_code=404, detail="Detalle no existe")
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
