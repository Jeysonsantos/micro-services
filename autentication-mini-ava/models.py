from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from config import Base

class User(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, index=True)
    id_aluno_professor = Column(Integer)
    nome = Column(String)
    senha = Column(String)
    tipo = Column(String)

class login(BaseModel):
    usuario: str
    senha: str

class retorno(BaseModel):
    idUsuario: int
    tipoUsuario: str
    nome: str   