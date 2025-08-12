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

    @staticmethod
    def validar_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11:
            return False

        # Check for known invalid CPFs (all digits are the same)
        if cpf == cpf[0] * 11:
            return False

        # Validate first digit
        sum_ = 0
        for i in range(9):
            sum_ += int(cpf[i]) * (10 - i)
        digit1 = 11 - (sum_ % 11)
        if digit1 > 9:
            digit1 = 0
        if digit1 != int(cpf[9]):
            return False

        # Validate second digit
        sum_ = 0
        for i in range(10):
            sum_ += int(cpf[i]) * (11 - i)
        digit2 = 11 - (sum_ % 11)
        if digit2 > 9:
            digit2 = 0
        if digit2 != int(cpf[10]):
            return False

        return True