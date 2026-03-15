"""
Modelo ORM que representa la entidad Factura del sistema.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Factura(Base):
    """
    Representa una factura generada en el sistema.


    """

    __tablename__ = "factura"

    id_factura = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    total = Column(Float, nullable=False)

    fecha_pago = Column(DateTime)

    id_orden = Column(UUID(as_uuid=True), ForeignKey("orden.id_orden"), nullable=False)

    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )

    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    fecha_actualizacion = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    orden = relationship("Orden", back_populates="factura")

    usuario = relationship("Usuario", back_populates="facturas")
