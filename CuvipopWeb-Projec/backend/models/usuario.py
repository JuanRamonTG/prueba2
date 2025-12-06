from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from database import Base
import enum

class RolEnum(enum.Enum):
    cliente = "cliente"
    admin = "admin"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.cliente)
    fecha_registro = Column(TIMESTAMP)


