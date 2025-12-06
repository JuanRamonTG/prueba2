from fastapi import APIRouter, Depends
from dependencies import get_current_user, solo_admin, get_db
from sqlalchemy.orm import Session
from models.producto import Producto

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()

    resultado = []
    for p in productos:
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": float(p.precio) if p.precio is not None else 0.0,
            "imagen": p.imagen or "",
            "categoria": p.categoria.name if p.categoria is not None else None,
            "disponible": bool(p.disponible)
        })

    return resultado


@router.post("/crear")
def crear_producto(user = Depends(solo_admin)):
    return {"mensaje": "Producto creado por admin"}
