from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.Mesa import Mesa

db = SessionLocal()


def crear_mesa(numero_mesa: str, id_usuario_creacion: UUID, estado: str) -> Mesa:
    """
    Crea una nueva mesa en el sistema.

    Parametros
    ----------
    numero_mesa : str
        El numero o nombre de la mesa a crear.
    id_usuario_creacion : UUID
        Llave primaria del usuario que crea la mesa.
    estado : str
        Estado de la mesa (DISPONIBLE, OCUPADA, RESERVADA).

    Returns
    -------
    Mesa
        Retorna la mesa creada.
    """

    mesa_limpia = numero_mesa.strip().upper()
    nombre_mesa = db.query(Mesa).filter(Mesa.numero_mesa == mesa_limpia).first()

    if nombre_mesa:
        raise ValueError("La Mesa ya existe")

    mesa = Mesa(
        numero_mesa=mesa_limpia,
        estado=estado.strip(),
        id_usuario_creacion=id_usuario_creacion,
    )

    db.add(mesa)
    db.commit()
    db.refresh(mesa)
    return mesa


def actualizar_estado(id_mesa: UUID, nuevo_estado: str) -> Optional[Mesa]:
    """
    Actualiza el estado de una mesa existente.

    Parametros
    ----------
    id_mesa : UUID
        llave primaria de la mesa a actualizar.
    nuevo_estado : str
        Nuevo estado a asignar (DISPONIBLE, OCUPADA, RESERVADA).

    Returns
    -------
    Optional[Mesa]
        La mesa con el estado actualizado o None si no se encuentra.
    """
    estado_mesas = ["DISPONIBLE", "OCUPADA", "RESERVADA"]

    mesa = obtener_por_id(id_mesa)

    if not mesa:
        return None

    estado_limpia = nuevo_estado.strip().upper()

    if estado_limpia not in estado_mesas:
        raise ValueError(
            f"El estado ingresado no es válido. "
            f"Los estados permitidos son: DISPONIBLE OCUPADA RESERVADA "
        )

    mesa.estado = estado_limpia

    db.commit()
    db.refresh(mesa)
    return mesa


def obtener_por_id(id_mesa: UUID) -> Optional[Mesa]:
    """
    Busca una mesa

    Parametros
    ----------
    id_mesa : UUID
        llave primaria de la mesa

    Returns
    -------
    Optional[Mesa]
        La mesa encontrada o None si no existe.
    """
    return db.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()


def obtener_todos() -> List[Mesa]:
    """
    Retorna una lista de todas las mesas

    Returns
    -------
    List[Mesa]
        Lista de todos los objetos Mesa en la base de datos.
    """
    return db.query(Mesa).all()


def actualizar(
    id_mesa: UUID,
    id_usuario_edicion: UUID,
    **kwargs: dict,
) -> Optional[Mesa]:
    """
    Actualiza campos de una mesa existente

    parametros
    ----------
    id_mesa : UUID
        Identificador de la mesa a editar.
    id_usuario_edicion : UUID
        Identificador del usuario que realiza el cambio.
    **kwargs : dict
        Diccionario de campos y valores a actualizar.

    Returns
    -------
    Optional[Mesa]
        La mesa editada o None si no se encuentra.
    """
    mesa = obtener_por_id(id_mesa)
    if not mesa:
        return None
    for key, value in kwargs.items():
        setattr(mesa, key, value)
    mesa.id_usuario_edicion = id_usuario_edicion
    db.commit()
    db.refresh(mesa)

    return mesa


def eliminar(id_mesa: UUID) -> bool:
    """
    Elimina una mesa del sistema

    Parametros
    ----------
    id_mesa : UUID
        Identificador de la mesa a eliminar.

    Returns
    -------
    bool
        True si la eliminación fue exitosa, False de lo contrario.
    """
    mesa = obtener_por_id(id_mesa)
    if not mesa:
        return False
    db.delete(mesa)
    db.commit()
    return True
