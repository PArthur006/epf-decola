from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base

class Voo(Base):
    __tablename__ = "voos"

    numero_voo = Column(String, primary_key=True, index=True)
    preco = Column(Float, nullable=False)
    data_partida = Column(DateTime, nullable=False)
    data_chegada = Column(DateTime, nullable=False)
    assentos_total = Column(Integer, nullable=False)
    comp_aerea = Column(String, nullable=False)
    assentos_ocupados = Column(JSON, nullable=False, default=[])
    
    destino_id = Column(Integer, ForeignKey("destinos.id"))
    destino = relationship("Destino")
    reservas = relationship("Reserva", back_populates="voo")

    @property
    def assentos_disp(self):
        return self.assentos_total - len(self.assentos_ocupados)
