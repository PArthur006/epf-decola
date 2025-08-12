from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL do banco de dados SQLite. O arquivo de banco de dados será 'decola.db' dentro da pasta 'data'.
DATABASE_URL = "sqlite:///./data/decola.db"

# Cria uma instância do motor do banco de dados.
# O argumento connect_args é necessário para SQLite em ambientes multi-thread (como o Bottle).
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configura uma classe SessionLocal para criar sessões de banco de dados.
# autocommit=False: As transações não são confirmadas automaticamente.
# autoflush=False: As operações não são enviadas automaticamente para o banco de dados.
# bind=engine: Associa a sessão ao motor do banco de dados criado.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma base declarativa para os modelos do SQLAlchemy.
# Os modelos de banco de dados herdarão desta classe.
Base = declarative_base()

def get_db():
    """
    Função geradora que fornece uma sessão de banco de dados.
    
    Esta função é usada para obter uma sessão de banco de dados para cada requisição.
    A sessão é fechada automaticamente após o uso, garantindo a liberação de recursos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
