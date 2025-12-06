from sqlalchemy import Column, Integer, String, Text, DECIMAL, Enum, Boolean
from database import Base
import enum

class CategoriaEnum(enum.Enum):
    helado = "helado"
    snack = "snack"

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(DECIMAL(10,2), nullable=False)
    imagen = Column(String(255))
    categoria = Column(Enum(CategoriaEnum), nullable=False)
    disponible = Column(Boolean, default=True)
