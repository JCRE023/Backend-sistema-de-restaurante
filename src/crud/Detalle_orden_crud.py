from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.detalle_orden import Detalle_orden
from src.entities.Orden import Orden
from src.entities.producto import Producto


class Detalle_orden_crud:
    """
    Clase para gestionar las operaciones de persistencia de la entidad Detalle_orden.
    Incluye validaciones de negocio sobre la orden y el producto asociados.
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio CRUD con una sesión de base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
        """
        self.db = db

    def crear_detalle(
        self, id_orden: UUID, id_producto: UUID, cantidad: int
    ) -> Detalle_orden:
        """
        Crea un nuevo detalle dentro de una orden existente.

        Args:
            id_orden (UUID): Identificador de la orden a la que pertenece el detalle.
            id_producto (UUID): Identificador del producto solicitado.
            cantidad (int): Cantidad de unidades (debe ser mayor a cero).

        Returns:
            Detalle_orden: El detalle recién creado y persistido.

        Raises:
            ValueError: Si la cantidad es inválida, la orden no existe o el producto no existe.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        orden = self.db.query(Orden).filter(Orden.id_orden == id_orden).first()
        if not orden:
            raise ValueError("La orden especificada no existe.")
        if orden.estado != "abierta":
            raise ValueError(
                "Solo se pueden agregar detalles a órdenes en estado 'abierta'."
            )

        producto = (
            self.db.query(Producto).filter(Producto.id_producto == id_producto).first()
        )
        if not producto:
            raise ValueError("El producto especificado no existe.")

        detalle = Detalle_orden(
            id_orden=id_orden,
            id_producto=id_producto,
            cantidad=cantidad,
        )

        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_detalle(self, id_detalle: UUID) -> Optional[Detalle_orden]:
        """
        Busca un detalle específico por su identificador único.

        Args:
            id_detalle (UUID): ID del detalle a buscar.

        Returns:
            Optional[Detalle_orden]: El detalle si se encuentra, de lo contrario None.
        """
        return (
            self.db.query(Detalle_orden)
            .filter(Detalle_orden.id_detalle == id_detalle)
            .first()
        )

    def obtener_detalles_por_orden(self, id_orden: UUID) -> List[Detalle_orden]:
        """
        Retorna todos los detalles asociados a una orden específica.

        Args:
            id_orden (UUID): ID de la orden cuyos detalles se quieren consultar.

        Returns:
            List[Detalle_orden]: Lista de detalles de la orden.
        """
        return (
            self.db.query(Detalle_orden)
            .filter(Detalle_orden.id_orden == id_orden)
            .all()
        )

    def obtener_detalles(self, skip: int = 0, limit: int = 100) -> List[Detalle_orden]:
        """
        Retorna una lista paginada de todos los detalles de órdenes.

        Args:
            skip (int): Cantidad de registros a omitir.
            limit (int): Cantidad máxima de registros a retornar.

        Returns:
            List[Detalle_orden]: Lista de objetos Detalle_orden.
        """
        return self.db.query(Detalle_orden).offset(skip).limit(limit).all()

    def actualizar_detalle(
        self, id_detalle: UUID, cantidad: int
    ) -> Optional[Detalle_orden]:
        """
        Actualiza la cantidad de un detalle existente.

        Args:
            id_detalle (UUID): ID del detalle a modificar.
            cantidad (int): Nueva cantidad de unidades (debe ser mayor a cero).

        Returns:
            Optional[Detalle_orden]: El detalle actualizado o None si no existe.

        Raises:
            ValueError: Si la cantidad es inválida o la orden ya no está abierta.
        """
        detalle = self.obtener_detalle(id_detalle)
        if not detalle:
            return None

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        orden = self.db.query(Orden).filter(Orden.id_orden == detalle.id_orden).first()
        if orden and orden.estado != "abierta":
            raise ValueError(
                "No se puede modificar un detalle de una orden que no está 'abierta'."
            )

        detalle.cantidad = cantidad

        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def eliminar_detalle(self, id_detalle: UUID) -> bool:
        """
        Elimina un detalle de la base de datos.

        Args:
            id_detalle (UUID): ID del detalle a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False si el detalle no existía.

        Raises:
            ValueError: Si la orden asociada ya no está en estado 'abierta'.
        """
        detalle = self.obtener_detalle(id_detalle)
        if not detalle:
            return False

        orden = self.db.query(Orden).filter(Orden.id_orden == detalle.id_orden).first()
        if orden and orden.estado != "abierta":
            raise ValueError(
                "No se puede eliminar un detalle de una orden que no está 'abierta'."
            )

        self.db.delete(detalle)
        self.db.commit()
        return True
