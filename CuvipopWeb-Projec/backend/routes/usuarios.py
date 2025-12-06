from fastapi import APIRouter, Depends
from dependencies import get_current_user, solo_admin
from models.usuario import Usuario  # ✔ Import válido aunque no se use aún

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# ----------------------------
# PERFIL DEL USUARIO LOGUEADO
# ----------------------------
@router.get("/perfil")
def ver_mi_perfil(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "nombre": user.nombre,
        "correo": user.correo,
        "rol": user.rol
    }

# ----------------------------
# SOLO ADMIN
# ----------------------------
@router.post("/admin-only")
def solo_admin_ruta(user = Depends(solo_admin)):
    return {"mensaje": "Bienvenido administrador"}
