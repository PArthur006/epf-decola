from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base
from datetime import datetime

class Reserva(Base):
    """Representa uma reserva de assento em um voo feita por um usuário."""
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True, doc="Identificador único da reserva.")
    assento = Column(String, nullable=False, doc="Número do assento reservado.")
    status = Column(String, default="Pendente", doc="Status atual da reserva (e.g., 'Pendente', 'Confirmada', 'Cancelada').")
    data_reserva = Column(DateTime, default=datetime.now, doc="Data e hora em que a reserva foi criada.")

    user_id = Column(String, ForeignKey("users.id"), doc="ID do usuário que fez a reserva.")
    voo_id = Column(String, ForeignKey("voos.numero_voo"), doc="Número do voo para o qual a reserva foi feita.")

    user = relationship("User", back_populates="reservas", doc="Objeto User associado a esta reserva.")
    voo = relationship("Voo", doc="Objeto Voo associado a esta reserva.")
    pagamento = relationship("Pagamento", back_populates="reserva", uselist=False, doc="Objeto Pagamento associado a esta reserva.")
