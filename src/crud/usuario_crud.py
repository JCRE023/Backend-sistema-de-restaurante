"""
CRUD para la entidad Usuario.
Incluye creación, autenticación y operaciones básicas.
"""

import hashlib
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.Usuario import Usuario


def _hash_contrasena(contrasena: str) -> str:
    """Genera un hash SHA-256 de la contraseña."""
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def crear(
    db: Session,
    username: str,
    password: str,
    rol: str = "usuario",
) -> Usuario:
    """
    Crea un nuevo usuario inyectando la sesión 'db'.
    """
    # Usamos la sesión 'db' que viene del router
    existente = (
        db.query(Usuario)
        .filter(Usuario.username == username.strip())
        .first()
    )

    if existente:
        raise ValueError("El usuario ya existe")

    usuario = Usuario(
        username=username.strip(),
        password=_hash_contrasena(password),
        rol=rol.strip(),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def login(db: Session, username: str, password: str) -> Optional[Usuario]:
    """Verifica las credenciales usando la sesión inyectada."""
    usuario = obtener_por_username(db, username)

    if not usuario:
        return None

    if usuario.password != _hash_contrasena(password):
        return None

    return usuario


def obtener_por_id(db: Session, id_usuario: UUID) -> Optional[Usuario]:
    """Obtiene un usuario por su ID."""
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_por_username(db: Session, username: str) -> Optional[Usuario]:
    """Obtiene un usuario por su nombre de usuario."""
    return (
        db.query(Usuario)
        .filter(Usuario.username == username.strip())
        .first()
    )


def obtener_todos(db: Session) -> List[Usuario]:
    """Obtiene todos los usuarios registrados."""
    return db.query(Usuario).all()


def actualizar(
    db: Session,
    id_usuario: UUID,
    username: Optional[str] = None,
    password: Optional[str] = None,
    rol: Optional[str] = None,
) -> Optional[Usuario]:
    """Actualiza los datos de un usuario."""
    usuario = obtener_por_id(db, id_usuario)

    if not usuario:
        return None

    if username is not None:
        usuario.username = username.strip()

    if password is not None:
        usuario.password = _hash_contrasena(password)

    if rol is not None:
        usuario.rol = rol.strip()

    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar(db: Session, id_usuario: UUID) -> bool:
    """Elimina un usuario de la base de datos."""
    usuario = obtener_por_id(db, id_usuario)

    if not usuario:
        return False

    db.delete(usuario)
    db.commit()
    return True