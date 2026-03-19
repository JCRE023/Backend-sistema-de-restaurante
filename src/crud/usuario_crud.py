"""
CRUD para la entidad Usuario.
Incluye creación, autenticación y operaciones básicas.
"""

import hashlib
from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.Usuario import Usuario

db = SessionLocal()


def _hash_contrasena(contrasena: str) -> str:
    """
    Genera un hash SHA-256 de la contraseña.

    Parameters
    ----------
    contrasena : str
        Contraseña en texto plano.

    Returns
    -------
    str
        Contraseña hasheada.
    """
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def crear(
    username: str,
    password: str,
    rol: str = "usuario",
) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.

    Parameters
    ----------
    username : str
        Nombre de usuario.
    password : str
        Contraseña en texto plano (será hasheada).
    rol : str, optional
        Rol del usuario.

    Returns
    -------
    Usuario
        Usuario creado.

    Raises
    ------
    ValueError
        Si el usuario ya existe.
    """

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


def login(username: str, password: str) -> Optional[Usuario]:
    """
    Verifica las credenciales de un usuario.

    Parameters
    ----------
    username : str
        Nombre de usuario.
    password : str
        Contraseña en texto plano.

    Returns
    -------
    Optional[Usuario]
        Usuario si las credenciales son correctas, de lo contrario None.
    """

    usuario = obtener_por_username(username)

    if not usuario:
        return None

    if usuario.password != _hash_contrasena(password):
        return None

    return usuario


def obtener_por_id(id_usuario: UUID) -> Optional[Usuario]:
    """
    Obtiene un usuario por su ID.

    Parameters
    ----------
    id_usuario : UUID
        Identificador del usuario.

    Returns
    -------
    Optional[Usuario]
        Usuario encontrado o None.
    """
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_por_username(username: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por su nombre de usuario.

    Parameters
    ----------
    username : str
        Nombre de usuario.

    Returns
    -------
    Optional[Usuario]
        Usuario encontrado o None.
    """
    return (
        db.query(Usuario)
        .filter(Usuario.username == username.strip())
        .first()
    )


def obtener_todos() -> List[Usuario]:
    """
    Obtiene todos los usuarios registrados.

    Returns
    -------
    List[Usuario]
        Lista de usuarios.
    """
    return db.query(Usuario).all()


def actualizar(
    id_usuario: UUID,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    rol: Optional[str] = None,
) -> Optional[Usuario]:
    """
    Actualiza los datos de un usuario.

    Parameters
    ----------
    id_usuario : UUID
        Identificador del usuario.
    username : str, optional
        Nuevo nombre de usuario.
    password : str, optional
        Nueva contraseña.
    rol : str, optional
        Nuevo rol.

    Returns
    -------
    Optional[Usuario]
        Usuario actualizado o None si no existe.
    """

    usuario = obtener_por_id(id_usuario)

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


def eliminar(id_usuario: UUID) -> bool:
    """
    Elimina un usuario de la base de datos.

    Parameters
    ----------
    id_usuario : UUID
        Identificador del usuario.

    Returns
    -------
    bool
        True si se eliminó correctamente, False si no existe.
    """

    usuario = obtener_por_id(id_usuario)

    if not usuario:
        return False

    db.delete(usuario)
    db.commit()

    return True