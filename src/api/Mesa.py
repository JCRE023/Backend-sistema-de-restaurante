import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud.Mesa_crud import MesaCRUD

router = APIRouter(prefix="/mesas", tags=["Mesas"])


class MesaBase(BaseModel):
    numero_mesa: str
    estado: str = "DISPONIBLE"


class MesaCreate(MesaBase):
    id_usuario_creacion: UUID


class MesaUpdate(BaseModel):
    estado: Optional[str] = None
    id_usuario_edicion: UUID


class MesaRead(MesaBase):
    model_config = ConfigDict(from_attributes=True)
    id_mesa: UUID
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: datetime.datetime


@router.post("/", response_model=MesaRead, status_code=status.HTTP_201_CREATED)
def crear_nueva_mesa(data: MesaCreate, db: DbSession):
    """Crea una mesa en el sistema usando el MesaCRUD."""
    crud = MesaCRUD(db)
    try:
        return crud.crear_mesa(
            numero_mesa=data.numero_mesa,
            id_usuario_creacion=data.id_usuario_creacion,
            estado=data.estado,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[MesaRead])
def listar_todas_las_mesas(db: DbSession):
    """Obtiene el listado completo de mesas desde Neon."""
    crud = MesaCRUD(db)
    return crud.obtener_todas()


@router.get("/{id_mesa}", response_model=MesaRead)
def obtener_mesa_por_id(id_mesa: UUID, db: DbSession):
    """Busca una mesa específica por su UUID."""
    crud = MesaCRUD(db)
    mesa = crud.obtener_por_id(id_mesa)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa


@router.put("/{id_mesa}", response_model=MesaRead)
def actualizar_datos_mesa(id_mesa: UUID, data: MesaUpdate, db: DbSession):
    """Actualiza el estado u otros campos de la mesa."""
    crud = MesaCRUD(db)
    update_data = data.model_dump(exclude_unset=True)
    update_data.pop("id_usuario_edicion")

    mesa = crud.actualizar_mesa(
        id_mesa=id_mesa, id_usuario_edicion=data.id_usuario_edicion, **update_data
    )
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa


@router.delete("/{id_mesa}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mesa(id_mesa: UUID, db: DbSession):
    """Elimina la mesa del sistema."""
    from src.entities.Orden import Orden
    from src.entities.Factura import Factura
    from src.entities.detalle_orden import Detalle_orden

    ordenes = db.query(Orden).filter(Orden.id_mesa == id_mesa).all()
    for orden in ordenes:
        db.query(Factura).filter(Factura.id_orden == orden.id_orden).delete()
        db.query(Detalle_orden).filter(Detalle_orden.id_orden == orden.id_orden).delete()
        db.delete(orden)
    db.flush()

    crud = MesaCRUD(db)
    if not crud.eliminar(id_mesa):
        raise HTTPException(status_code=404, detail="La mesa no existe")
    return None
