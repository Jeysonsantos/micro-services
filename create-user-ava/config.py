from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases import Database

# Modelo do usuário
Base = declarative_base()

# Configuração do banco de dados
DATABASE_URL = "mysql://root:root@localhost:3306/gerenciamento-matricula"
database = Database(DATABASE_URL)

# Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)