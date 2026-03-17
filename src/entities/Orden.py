import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base


class Orden(Base):
    __tablename__ = "orden"

    id_orden = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    estado = Column(String(50), nullable=False, default="abierta")

    id_mesa = Column(UUID(as_uuid=True), ForeignKey("mesa.id_mesa"), nullable=False)
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )

    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    mesa = relationship("Mesa", back_populates="orden")
    usuario = relationship("Usuario", foreign_keys=[id_usuario])
    detalle = relationship("Detalle_orden", back_populates="orden")
    factura = relationship("Factura", uselist=False, back_populates="orden")
