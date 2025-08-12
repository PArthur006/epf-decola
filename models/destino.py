from sqlalchemy import Column, Integer, String
from data.database import Base

class Destino(Base):
    """Representa um destino de voo, incluindo informações da cidade, país, aeroporto e imagem."""
    __tablename__ = "destinos"

    id = Column(Integer, primary_key=True, index=True, doc="Identificador único do destino.")
    cidade = Column(String, nullable=False, doc="Nome da cidade do destino.")
    pais = Column(String, nullable=False, doc="Nome do país do destino.")
    aeroporto = Column(String, nullable=False, doc="Código do aeroporto do destino.")
    imagem = Column(String, nullable=False, doc="Caminho da imagem representativa do destino.")
