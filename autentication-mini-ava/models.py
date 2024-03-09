from sqlalchemy import Column, Integer, String,create_engine
from databases import Database
import sqlalchemy
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql://root:root@localhost:3306/gerenciamento-matricula"
database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

usuarios = sqlalchemy.Table(
    "usuarios",
    metadata,
    Column("id_usuario", Integer, primary_key=True),
    Column("cpf", String),
    Column("id_aluno_professor", Integer),
    Column("nome", String),
    Column("senha", String),
    Column("tipo", String),
)