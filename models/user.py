from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from data.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    birthdate = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    nationality = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    reservas = relationship("Reserva", back_populates="user")