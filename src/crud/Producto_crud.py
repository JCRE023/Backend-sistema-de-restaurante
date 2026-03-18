from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.producto import Producto
from src.entities.Usuario import Usuario


class ProductoCRUD:
    """
    Clase para gestionar las operaciones de persistencia de la entidad Producto.
    Incluye validaciones de negocio y auditoría de usuarios.
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio CRUD con una sesión de base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
        """
        self.db = db

    def crear_producto(
        self,
        nombre: str,
        precio: float,
        categoria: str,
        id_usuario_creacion: UUID,
        descripcion: str = None,
    ) -> Producto:
        """
        Crea un nuevo producto en el sistema tras validar los datos de entrada.

        Args:
            nombre (str): Nombre único para el producto.
            precio (float): Valor monetario (debe ser mayor a cero).
            categoria (str): Etiqueta de categorización.
            id_usuario_creacion (UUID): Identificador del usuario que registra el producto.
            descripcion (str, optional): Detalle adicional del producto.

        Returns:
            Producto: El objeto producto recién creado y persistido.

        Raises:
            ValueError: Si el nombre está vacío, el precio es inválido o el usuario no existe.
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del producto es obligatorio.")
        if precio <= 0:
            raise ValueError("El precio debe ser un valor positivo.")

        usuario = (
            self.db.query(Usuario)
            .filter(Usuario.id_usuario == id_usuario_creacion)
            .first()
        )
        if not usuario:
            raise ValueError(
                "El usuario creador especificado no existe en la base de datos."
            )

        producto = Producto(
            nombre=nombre.strip(),
            descripcion=descripcion.strip() if descripcion else None,
            precio=precio,
            categoria=categoria.strip(),
            id_usuario_creacion=id_usuario_creacion,
        )

        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(self, producto_id: UUID) -> Optional[Producto]:
        """
        Busca un producto específico por su identificador único.

        Args:
            producto_id (UUID): ID del producto a buscar.

        Returns:
            Optional[Producto]: El producto si se encuentra, de lo contrario None.
        """
        return (
            self.db.query(Producto).filter(Producto.id_producto == producto_id).first()
        )

    def obtener_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """
        Retorna una lista paginada de todos los productos.

        Args:
            skip (int): Cantidad de registros a omitir.
            limit (int): Cantidad máxima de registros a retornar.

        Returns:
            List[Producto]: Lista de objetos Producto.
        """
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def actualizar_producto(
        self, producto_id: UUID, id_usuario_edita: UUID, **kwargs
    ) -> Optional[Producto]:
        """
        Actualiza los campos de un producto existente y registra quién realizó el cambio.

        Args:
            producto_id (UUID): ID del producto a modificar.
            id_usuario_edita (UUID): ID del usuario que realiza la edición.
            **kwargs: Diccionario de campos a actualizar (nombre, precio, etc.).

        Returns:
            Optional[Producto]: El producto actualizado o None si no existe.

        Raises:
            ValueError: Si el usuario editor no existe o los datos nuevos son inválidos.
        """
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None

        usuario = (
            self.db.query(Usuario)
            .filter(Usuario.id_usuario == id_usuario_edita)
            .first()
        )
        if not usuario:
            raise ValueError("El usuario editor no existe.")

        if "precio" in kwargs and kwargs["precio"] <= 0:
            raise ValueError("El nuevo precio debe ser mayor a 0.")

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)

        producto.id_usuario_edita = id_usuario_edita

        self.db.commit()
        self.db.refresh(producto)
        return producto

    def eliminar_producto(self, producto_id: UUID) -> bool:
        """
        Elimina un producto de la base de datos.

        Args:
            producto_id (UUID): ID del producto a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False si el producto no existía.
        """
        producto = self.obtener_producto(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
