import json
import os
from datetime import datetime
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class User:
    def __init__(self, user_id: str, name: str, email: str, birthdate: str,
                 cpf: str, nationality: str, phone: Optional[str] = None):
        self.id = user_id
        self.name = name
        self.email = email
        self.birthdate = birthdate
        self.cpf = cpf
        self.nationality = nationality
        self.phone = phone
        self.reservas = []  # lista de Reserva

    def add_reserva(self, reserva):
        self.reservas.append(reserva)

    def remove_reserva(self, reserva_id):
        self.reservas = [r for r in self.reservas if r.id_reserva != reserva_id]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'birthdate': self.birthdate,
            'cpf': self.cpf,
            'nationality': self.nationality,
            'phone': self.phone,
            'reservas': [r.id_reserva for r in self.reservas]  # armazenar só IDs das reservas
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            user_id=data['id'],
            name=data['name'],
            email=data['email'],
            birthdate=data['birthdate'],
            cpf=data['cpf'],
            nationality=data['nationality'],
            phone=data.get('phone')
        )
        # reservas serão ligadas depois pelo modelo
        return user

class UserModel:
    FILE_PATH = os.path.join(DATA_DIR, 'users.json')

    def __init__(self):
        self.users = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [User.from_dict(item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.users], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.users

    def get_by_id(self, user_id: str):
        return next((u for u in self.users if u.id == user_id), None)

    def add_user(self, user: User):
        self.users.append(user)
        self._save()

    def update_user(self, updated_user: User):
        for i, user in enumerate(self.users):
            if user.id == updated_user.id:
                self.users[i] = updated_user
                self._save()
                break

    def delete_user(self, user_id: str):
        self.users = [u for u in self.users if u.id != user_id]
        self._save()
