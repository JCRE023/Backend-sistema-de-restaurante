import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.entities.Usuario import Usuario
from src.crud import usuario_crud


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: UUID
    username: str
    rol: str
    fecha_creacion: Optional[datetime.datetime]


class UsuarioCreate(BaseModel):
    username: str
    password: str
    rol: str


@router.get("", response_model=List[UsuarioRead])
def listar_usuarios(db: DbSession):
    """1. GET lista: Obtiene todos los usuarios de Neon."""
    return usuario_crud.obtener_todos(db)


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(db: DbSession, id_usuario: UUID):
    """2. GET por id: Busca un usuario específico."""
    u = usuario_crud.obtener_por_id(db, id_usuario)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return u


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(db: DbSession, data: UsuarioCreate):
    """3. POST: Registra un nuevo usuario con contraseña hasheada."""
    try:
        return usuario_crud.crear(db, data.username, data.password, data.rol)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(db: DbSession, id_usuario: UUID, data: UsuarioCreate):
    """4. PUT: Actualiza los datos de un usuario."""
    u = usuario_crud.actualizar(
        db, 
        id_usuario, 
        username=data.username, 
        password=data.password, 
        rol=data.rol
    )
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return u


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(db: DbSession, id_usuario: UUID):
    """5. DELETE: Elimina físicamente el usuario."""
    if not usuario_crud.eliminar(db, id_usuario):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no existe"
        )
    return None