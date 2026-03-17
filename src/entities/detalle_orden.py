import uuid
from database.config import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Detalle_orden(Base):
    __tablename__ = "detalle_orden"

    id_detalle = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cantidad = Column(Integer, default=0, nullable=False)

    id_orden = Column(UUID(as_uuid=True), ForeignKey("orden.id_orden"), nullable=False)
    id_producto = Column(
        UUID(as_uuid=True), ForeignKey("producto.id_producto"), nullable=False
    )

    orden = relationship("Orden", back_populates="detalle")
    producto = relationship("Producto", back_populates="detalle")
