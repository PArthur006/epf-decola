from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base
from datetime import datetime

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    assento = Column(String, nullable=False)
    status = Column(String, default="Pendente")
    data_reserva = Column(DateTime, default=datetime.now)

    user_id = Column(String, ForeignKey("users.id"))
    voo_id = Column(String, ForeignKey("voos.numero_voo"))

    user = relationship("User", back_populates="reservas")
    voo = relationship("Voo")
    pagamento = relationship("Pagamento", back_populates="reserva", uselist=False)