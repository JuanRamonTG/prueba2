from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Text
from database import Base

class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    latitud = Column(DECIMAL(10,7))
    longitud = Column(DECIMAL(10,7))
    referencia = Column(Text)
