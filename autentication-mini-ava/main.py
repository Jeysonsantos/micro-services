from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import User, login, retorno
from config import SessionLocal

# Configuração do banco de dados

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de login
@app.post("/login/")
async def login(login: login):
    db = SessionLocal()
    usuario = db.query(User).filter(User.cpf == login.usuario).first()
    db.close()
    if usuario is None or login.senha != usuario.senha:
        return JSONResponse(status_code=401, content={"message": "Invalid credentials"})
    else:
        return retorno(idUsuario=usuario.id_usuario, tipoUsuario=usuario.tipo, nome=usuario.nome)

#inicializar - uvicorn main:app --reload