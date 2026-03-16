"""
Modelo ORM que representa la entidad Usuario del sistema.
"""

import uuid

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Usuario(Base):
    """
    Representa un usuario dentro del sistema.
    """

    __tablename__ = "usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(100), nullable=False, unique=True)

    password = Column(String(255), nullable=False)

    rol = Column(String(50), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)

    fecha_actualizacion = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    facturas = relationship("Factura", back_populates="usuario")
