from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Enum, DECIMAL, Text, TIMESTAMP
from database import Base
import enum

class TipoEntregaEnum(enum.Enum):
    llevar = "llevar"
    domicilio = "domicilio"

class MetodoPagoEnum(enum.Enum):
    efectivo = "efectivo"
    tarjeta = "tarjeta"

class EstadoPedidoEnum(enum.Enum):
    pendiente = "pendiente"
    en_preparacion = "en_preparacion"
    en_camino = "en_camino"
    entregado = "entregado"
    cancelado = "cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_pedido = Column(TIMESTAMP)
    fecha_programada = Column(Date, nullable=False)
    hora_programada = Column(Time, nullable=False)
    tipo_entrega = Column(Enum(TipoEntregaEnum), nullable=False)
    direccion = Column(Text)
    metodo_pago = Column(Enum(MetodoPagoEnum), nullable=False)
    monto_efectivo = Column(DECIMAL(10,2))
    total = Column(DECIMAL(10,2), nullable=False)
    estado = Column(Enum(EstadoPedidoEnum), default=EstadoPedidoEnum.pendiente)
