from sqlalchemy import Column, Integer, String
from data.database import Base

class Destino(Base):
    __tablename__ = "destinos"

    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    aeroporto = Column(String, nullable=False)
    imagem = Column(String, nullable=False)