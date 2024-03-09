from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# Configuração do banco de dados
DATABASE_URL = "mysql://root:root@localhost:3306/gerenciamento-matricula"
database = Database(DATABASE_URL)

# Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configuração do contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

# Função para criar token JWT
def create_jwt_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)  # Defina o tempo de expiração como necessário
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")  # Substitua "secret" por sua chave secreta
    return encoded_jwt

# Função para obter usuário atual
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login/"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])  # Substitua "secret" por sua chave secreta
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    db = SessionLocal()
    user = db.query(User).filter(User.cpf == username).first()
    db.close()
    if user is None:
        raise credentials_exception
    return user

app = FastAPI()

# Rota de registro (signup)
@app.post("/signup/")
async def signup(cpf: str, senha: str, nome: str, tipo: str):
    db = SessionLocal()
    hashed_password = pwd_context.hash(senha)
    db_user = User(cpf=cpf, senha=hashed_password, nome=nome, tipo=tipo)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"cpf": db_user.cpf, "nome": db_user.nome, "tipo": db_user.tipo}

# Rota de login
@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    db = SessionLocal()
    user = db.query(User).filter(User.cpf == form_data.username).first()
    print(user)
    db.close()
    if(user is None):
        return JSONResponse(status_code=401, content={"message": "Invalid credentials"})

    

# Rota protegida para verificar a autenticação
@app.get("/protected/")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "You are authenticated!", "cpf": current_user.cpf, "nome": current_user.nome, "tipo": current_user.tipo}
