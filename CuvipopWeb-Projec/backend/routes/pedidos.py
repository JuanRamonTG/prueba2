from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, validator
from typing import List
from dependencies import get_db
from datetime import date, time
import datetime
from models.pedido import TipoEntregaEnum, MetodoPagoEnum

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


class ItemPedido(BaseModel):
    id: int
    cantidad: int
    precio: float


class PedidoCreate(BaseModel):
    items: List[ItemPedido]
    total: float
    fecha_programada: date
    hora_programada: time
    tipo_entrega: TipoEntregaEnum
    metodo_pago: MetodoPagoEnum

    @validator('hora_programada')
    def validar_hora(cls, v: time):
        # Permitir entre 11:00 y 19:30
        min_h = time(hour=11, minute=0)
        max_h = time(hour=19, minute=30)
        if v < min_h or v > max_h:
            raise ValueError('Hora debe estar entre 11:00 y 19:30')
        return v


@router.post("/")
def crear_pedido(pedido: PedidoCreate, db=Depends(get_db)):
    # Validación mínima ya realizada por Pydantic
    # Aquí se puede persistir en la BD usando los modelos Pedido y DetallePedido.
    return {
        "mensaje": "Pedido recibido",
        "total": pedido.total,
        "items": pedido.items,
        "fecha_programada": str(pedido.fecha_programada),
        "hora_programada": pedido.hora_programada.strftime('%H:%M'),
        "tipo_entrega": pedido.tipo_entrega.value,
        "metodo_pago": pedido.metodo_pago.value
    }
