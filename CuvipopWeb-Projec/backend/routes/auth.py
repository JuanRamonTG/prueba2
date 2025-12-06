from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database import SessionLocal
from models.usuario import Usuario
from security import hash_password, verify_password, create_access_token
from dependencies import get_current_user  # ✅ SOLO UNA VEZ

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# ----------------------------
# CONEXIÓN DB
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# SCHEMAS
# ----------------------------
class RegistroSchema(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

class LoginSchema(BaseModel):
    correo: EmailStr
    password: str

# ----------------------------
# REGISTRO
# ----------------------------
@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar(data: RegistroSchema, db: Session = Depends(get_db)):

    existe = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo = Usuario(
        nombre=data.nombre,
        correo=data.correo,
        password=hash_password(data.password),
        rol="cliente"
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario": {
            "id": nuevo.id,
            "nombre": nuevo.nombre,
            "correo": nuevo.correo,
            "rol": nuevo.rol
        }
    }

# ----------------------------
# LOGIN (NO PROTEGIDO ✅)
# ----------------------------
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(Usuario).filter(Usuario.correo == data.correo).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({
        "sub": user.correo,
        "rol": user.rol.value  # ✅ CORRECTO PARA JWT
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": user.rol.value
    }

# ----------------------------
# RUTA PROTEGIDA ✅
# ----------------------------
@router.get("/protegida")
def ruta_protegida(user=Depends(get_current_user)):
    return {
        "mensaje": "Acceso concedido",
        "usuario": user
    }
