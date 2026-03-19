from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.Orden import Orden
from src.entities.detalle_orden import Detalle_orden
from src.entities.Mesa import Mesa


class Orden_crud:
    """
    Clase para gestionar el flujo de órdenes, incluyendo la apertura de pedidos,
    la adición de productos y la liberación de mesas.
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
        """
        self.db = db

    def crear_orden(self, id_mesa: UUID, id_usuario: UUID) -> Orden:
        """
        Abre una nueva orden de servicio y marca la mesa como 'ocupada'.

        Args:
            id_mesa (UUID): Identificador de la mesa asignada.
            id_usuario (UUID): Identificador del mesero/usuario que abre la orden.

        Returns:
            Orden: La nueva orden creada.

        Raises:
            ValueError: Si la mesa no existe o ya está ocupada.
        """
        mesa = self.db.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()
        if not mesa:
            raise ValueError("La mesa especificada no existe.")
        if mesa.estado.upper() != "DISPONIBLE":
            raise ValueError(f"La mesa {mesa.numero_mesa} no está disponible.")

        nueva_orden = Orden(id_mesa=id_mesa, id_usuario=id_usuario, estado="abierta")

        mesa.estado = "ocupada"

        self.db.add(nueva_orden)
        self.db.commit()
        self.db.refresh(nueva_orden)
        return nueva_orden

    def agregar_item_a_orden(
        self, id_orden: UUID, id_producto: UUID, cantidad: int
    ) -> Detalle_orden:
        """
        Registra un producto y su cantidad dentro de una orden existente.

        Args:
            id_orden (UUID): Orden a la que pertenece el detalle.
            id_producto (UUID): Producto solicitado.
            cantidad (int): Cantidad de unidades (debe ser mayor a cero).

        Returns:
            Detalle_orden: El registro del detalle creado.

        Raises:
            ValueError: Si la cantidad es inválida.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        detalle = Detalle_orden(
            id_orden=id_orden, id_producto=id_producto, cantidad=cantidad
        )
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_orden(self, id_orden: UUID) -> Optional[Orden]:
        """
        Obtiene la información de una orden incluyendo sus relaciones.

        Args:
            id_orden (UUID): ID de la orden.

        Returns:
            Optional[Orden]: El objeto Orden o None.
        """
        return self.db.query(Orden).filter(Orden.id_orden == id_orden).first()

    def cerrar_orden(self, id_orden: UUID) -> Optional[Orden]:
        """
        Cambia el estado de la orden a 'cerrada' y libera la mesa asociada.

        Args:
            id_orden (UUID): ID de la orden a finalizar.

        Returns:
            Optional[Orden]: La orden actualizada o None.
        """
        orden = self.obtener_orden(id_orden)
        if not orden:
            return None

        orden.estado = "cerrada"

        mesa = self.db.query(Mesa).filter(Mesa.id_mesa == orden.id_mesa).first()
        if mesa:
            mesa.estado = "disponible"

        self.db.commit()
        self.db.refresh(orden)
        return orden
