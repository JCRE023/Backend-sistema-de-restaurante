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
    """
    1. GET lista: Obtiene todos los usuarios.
    """
    return db.query(Usuario).all()


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(db: DbSession, id_usuario: UUID):
    """
    2. GET por id: Busca un usuario por su UUID.
    """
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return usuario


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(db: DbSession, data: UsuarioCreate):
    """
    3. POST: Crea un nuevo usuario.
    """
    existente = (
        db.query(Usuario)
        .filter(Usuario.username == data.username.strip())
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
        )

    return usuario_crud.crear(data.username, data.password, data.rol)


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(db: DbSession, id_usuario: UUID, data: UsuarioCreate):
    """
    4. PUT: Actualiza un usuario.
    """
    usuario = usuario_crud.actualizar(
        id_usuario,
        nombre_usuario=data.username,
        contrasena=data.password,
        rol=data.rol,
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return usuario


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(db: DbSession, id_usuario: UUID):
    """
    5. DELETE: Elimina un usuario.
    """
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no existe",
        )

    db.delete(usuario)
    db.commit()
    return None