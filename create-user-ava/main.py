from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import User, UsuarioCreate
from config import SessionLocal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuração do banco de dados

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create_user/")
async def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    # Criar uma instância do modelo SQLAlchemy usando os dados do Pydantic
    # Transforma id_aluno_professor em long
    user.id_aluno_professor = int(user.id_aluno_professor)
    db_user = User(**user.dict())

    # Verificar se o usuário já existe
    user_exists = db.query(User).filter(User.cpf == user.cpf).first()
    id_exists = db.query(User).filter(User.id_aluno_professor == user.id_aluno_professor).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    if id_exists:
        raise HTTPException(status_code=400, detail="ID já cadastrado")

    # Adicionar a instância à sessão e fazer commit no banco de dados
    db.add(db_user)
    db.commit()

    return {"message": "Usuário criado com sucesso"}

#inicializar - uvicorn main:app --reload --port 8001

