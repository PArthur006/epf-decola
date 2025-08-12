from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base

class Voo(Base):
    """Representa um voo disponível no sistema, incluindo detalhes como preço, datas e assentos."""
    __tablename__ = "voos"

    numero_voo = Column(String, primary_key=True, index=True, doc="Número de identificação único do voo.")
    preco = Column(Float, nullable=False, doc="Preço do voo por assento.")
    data_partida = Column(DateTime, nullable=False, doc="Data e hora de partida do voo.")
    data_chegada = Column(DateTime, nullable=False, doc="Data e hora de chegada do voo.")
    assentos_total = Column(Integer, nullable=False, doc="Número total de assentos disponíveis no voo.")
    comp_aerea = Column(String, nullable=False, doc="Companhia aérea responsável pelo voo.")
    assentos_ocupados = Column(JSON, nullable=False, default=[], doc="Lista de assentos já ocupados no voo.")
    
    destino_id = Column(Integer, ForeignKey("destinos.id"), doc="ID do destino associado a este voo.")
    destino = relationship("Destino", doc="Objeto Destino associado a este voo.")
    reservas = relationship("Reserva", back_populates="voo", doc="Lista de reservas feitas para este voo.")

    @property
    def assentos_disp(self):
        """Retorna o número de assentos disponíveis no voo."""
        return self.assentos_total - len(self.assentos_ocupados)
