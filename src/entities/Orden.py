import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Orden(Base):
    __tablename__ = "orden"

    id_orden = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    estado = Column(String(50), nullable=False, default="abierta")

    id_mesa = Column(UUID(as_uuid=True), ForeignKey("mesa.id_mesa"), nullable=False)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)

    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    mesa = relationship("Mesa", back_populates="ordenes")
    usuario = relationship("Usuario", foreign_keys=[id_usuario])
    detalles = relationship("DetalleOrden", back_populates="orden")
    factura = relationship("Factura", uselist=False, back_populates="orden")
