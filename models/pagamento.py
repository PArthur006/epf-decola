from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base
from datetime import datetime

class Pagamento(Base):
    """Representa um registro de pagamento no sistema."""
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True, doc="Identificador único do pagamento.")
    valor = Column(Float, nullable=False, doc="Valor total do pagamento.")
    forma_pagamento = Column(String, nullable=False, doc="Método de pagamento utilizado (e.g., 'Cartão de Crédito', 'Boleto').")
    status = Column(String, default="Pendente", doc="Status atual do pagamento (e.g., 'Pendente', 'Aprovado', 'Recusado').")
    data_pagamento = Column(DateTime, default=datetime.now, doc="Data e hora em que o pagamento foi registrado.")

    reserva_id = Column(Integer, ForeignKey("reservas.id"), doc="ID da reserva associada a este pagamento.")
    reserva = relationship("Reserva", back_populates="pagamento", doc="Objeto Reserva associado a este pagamento.")
