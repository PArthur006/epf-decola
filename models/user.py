from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from data.database import Base

class User(Base):
    """Representa um usuário no sistema, incluindo suas informações pessoais e de autenticação."""
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, doc="Identificador único do usuário.")
    name = Column(String, nullable=False, doc="Nome completo do usuário.")
    email = Column(String, unique=True, index=True, nullable=False, doc="Endereço de e-mail único do usuário.")
    password = Column(String, nullable=False, doc="Senha hash do usuário.")
    birthdate = Column(String, nullable=False, doc="Data de nascimento do usuário.")
    cpf = Column(String, unique=True, nullable=False, doc="CPF único do usuário.")
    nationality = Column(String, nullable=False, doc="Nacionalidade do usuário.")
    phone = Column(String, nullable=True, doc="Número de telefone do usuário (opcional).")

    reservas = relationship("Reserva", back_populates="user", doc="Lista de reservas feitas pelo usuário.")

    @staticmethod
    def validar_cpf(cpf):
        """Valida um número de CPF.

        Args:
            cpf (str): O número de CPF a ser validado.

        Returns:
            bool: True se o CPF for válido, False caso contrário.
        """
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