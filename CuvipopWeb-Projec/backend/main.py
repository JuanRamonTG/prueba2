from fastapi import FastAPI
from routes import auth, productos   # solo los que existan
from routes import usuarios, pedidos
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="API Cuvipop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos (para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(usuarios.router)
app.include_router(pedidos.router)


# Servir la carpeta frontend (que está fuera de backend)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")