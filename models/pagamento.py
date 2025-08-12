from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base
from datetime import datetime

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    forma_pagamento = Column(String, nullable=False)
    status = Column(String, default="Pendente")
    data_pagamento = Column(DateTime, default=datetime.now)

    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    reserva = relationship("Reserva", back_populates="pagamento")
