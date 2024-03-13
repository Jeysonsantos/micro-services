from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from fastapi.middleware.cors import CORSMiddleware
# Configuração do banco de dados
DATABASE_URL = "mysql://root:root@localhost:3306/gerenciamento-matricula"
database = Database(DATABASE_URL)

# Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo do usuário
Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, index=True)
    id_aluno_professor = Column(Integer)
    nome = Column(String)
    senha = Column(String)
    tipo = Column(String)

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class login(BaseModel):
    usuario: str
    senha: str

class retorno(BaseModel):
    idUsuario: int
    tipoUsuario: str
    nome: str   
# Rota de login
@app.post("/login/")
async def login(login: login):
    print(login.usuario, login.senha)
    db = SessionLocal()
    usuario = db.query(User).filter(User.cpf == login.usuario).first()
    db.close()
    if usuario is None or login.senha != usuario.senha:
        return JSONResponse(status_code=401, content={"message": "Invalid credentials"})
    else:
        return retorno(idUsuario=usuario.id_usuario, tipoUsuario=usuario.tipo, nome=usuario.nome)


#inicializar - uvicorn main:app --reload
