import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud.Producto_crud import ProductoCRUD

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoBase(BaseModel):
    nombre: str
    precio: float
    categoria: str
    descripcion: Optional[str] = None


class ProductoCreate(ProductoBase):
    id_usuario_creacion: UUID


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    id_usuario_edicion: UUID


class ProductoRead(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    id_producto: UUID
    fecha_creacion: Optional[datetime.datetime]
    id_usuario_creacion: UUID


@router.get("", response_model=List[ProductoRead])
def listar_productos(db: DbSession):
    """GET lista de productos [cite: 12]"""
    crud = ProductoCRUD(db)
    return crud.obtener_productos()


@router.get("/{id_producto}", response_model=ProductoRead)
def obtener_producto(db: DbSession, id_producto: UUID):
    """GET por id de producto [cite: 13]"""
    crud = ProductoCRUD(db)
    p = crud.obtener_producto(id_producto)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return p


@router.post("", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(db: DbSession, body: ProductoCreate):
    """POST crear producto [cite: 14]"""
    crud = ProductoCRUD(db)
    return crud.crear_producto(**body.model_dump())


@router.put("/{id_producto}", response_model=ProductoRead)
def actualizar_producto(db: DbSession, id_producto: UUID, body: ProductoUpdate):
    """PUT editar producto [cite: 15]"""
    crud = ProductoCRUD(db)
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})
    p = crud.actualizar_producto(id_producto, body.id_usuario_edicion, **data)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo actualizar"
        )
    return p


@router.delete("/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(db: DbSession, id_producto: UUID):
    """DELETE eliminar producto [cite: 16]"""
    crud = ProductoCRUD(db)
    if not crud.eliminar_producto(id_producto):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado"
        )
