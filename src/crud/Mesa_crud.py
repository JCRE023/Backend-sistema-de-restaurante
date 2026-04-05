from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.Mesa import Mesa


class MesaCRUD:
    """
    Clase para gestionar las operaciones de persistencia de la entidad Mesa.
    Centraliza la lógica de estados y validación de duplicados.
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio con la sesión inyectada desde el endpoint.
        """
        self.db = db

    def crear_mesa(
        self, numero_mesa: str, id_usuario_creacion: UUID, estado: str = "DISPONIBLE"
    ) -> Mesa:
        """
        Crea una nueva mesa validando que el número no exista previamente.
        """
        mesa_limpia = numero_mesa.strip().upper()

        # Validación de duplicados usando la sesión inyectada
        existente = self.db.query(Mesa).filter(Mesa.numero_mesa == mesa_limpia).first()
        if existente:
            raise ValueError(f"La Mesa '{mesa_limpia}' ya existe en el sistema.")

        nueva_mesa = Mesa(
            numero_mesa=mesa_limpia,
            estado=estado.strip().upper(),
            id_usuario_creacion=id_usuario_creacion,
        )

        self.db.add(nueva_mesa)
        self.db.commit()
        self.db.refresh(nueva_mesa)
        return nueva_mesa

    def obtener_por_id(self, id_mesa: UUID) -> Optional[Mesa]:
        """Busca una mesa específica."""
        return self.db.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()

    def obtener_todas(self) -> List[Mesa]:
        """Retorna el listado completo de mesas."""
        return self.db.query(Mesa).all()

    def actualizar_estado(self, id_mesa: UUID, nuevo_estado: str) -> Optional[Mesa]:
        """
        Actualiza solo el estado de la mesa (útil para flujos rápidos).
        """
        estados_permitidos = ["DISPONIBLE", "OCUPADA", "RESERVADA"]
        estado_limpio = nuevo_estado.strip().upper()

        if estado_limpio not in estados_permitidos:
            raise ValueError(
                f"Estado no válido. Permitidos: {', '.join(estados_permitidos)}"
            )

        mesa = self.obtener_por_id(id_mesa)
        if not mesa:
            return None

        mesa.estado = estado_limpio
        self.db.commit()
        self.db.refresh(mesa)
        return mesa

    def actualizar_mesa(
        self, id_mesa: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Mesa]:
        """
        Actualización flexible de campos con registro de auditoría.
        """
        mesa = self.obtener_por_id(id_mesa)
        if not mesa:
            return None

        for key, value in kwargs.items():
            if hasattr(mesa, key):
                setattr(mesa, key, value)

        mesa.id_usuario_edicion = id_usuario_edicion

        self.db.commit()
        self.db.refresh(mesa)
        return mesa

    def eliminar(self, id_mesa: UUID) -> bool:
        """Elimina físicamente la mesa del sistema."""
        mesa = self.obtener_por_id(id_mesa)
        if not mesa:
            return False

        self.db.delete(mesa)
        self.db.commit()
        return True
