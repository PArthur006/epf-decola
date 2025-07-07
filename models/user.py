import json
import os
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class User:
    """Representa a entidade de um Usuário do sistema, com seus dados pessoais e uma lista de suas reservas."""
    def __init__(self, user_id: str, name: str, email: str, password: str, birthdate: str,
                 cpf: str, nationality: str, phone: Optional[str] = None):
        """Construtor da classe User."""
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password # OBS: É de conhecimento dos autores que em um projeto real, isso seria um hash.
        self.birthdate = birthdate
        self.cpf = cpf
        self.nationality = nationality
        self.phone = phone
        # A lista de reservas de um usuário é preenchida pelo ReservaModel.
        self.reservas = [] 

    def add_reserva(self, reserva):
        """Adiciona uma referência de uma reserva à lista do usuário."""
        self.reservas.append(reserva)

    def remove_reserva(self, reserva_id):
        """Remove uma referência de uma reserva da lista do usuário."""
        self.reservas = [r for r in self.reservas if r.id_reserva != reserva_id]

    def to_dict(self):
        """Converte o objeto User para um dicionário, para ser salvo em JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'birthdate': self.birthdate,
            'cpf': self.cpf,
            'nationality': self.nationality,
            'phone': self.phone,
            # No JSON, salvamos apenas os IDs das reservas para evitar redundância.
            'reservas': [r.id_reserva for r in self.reservas]  # armazenar só IDs das reservas
        }

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância de User a partir de um dicionário."""
        user = cls(
            user_id=data['id'],
            name=data['name'],
            email=data['email'],
            password=data['password'],
            birthdate=data['birthdate'],
            cpf=data['cpf'],
            nationality=data['nationality'],
            phone=data.get('phone')
        )
        # As reservas são associadas posteriormente pelo ReservaModel.
        return user

class UserModel:
    """Classe DAO responsável pela persistência e acesso aos dados dos usuários no arquivp 'user.json'."""
    FILE_PATH = os.path.join(DATA_DIR, 'users.json')

    def __init__(self):
        """Construtor que carrega todos os usuários para a memória."""
        self.users = self._load()


    def _load(self):
        """Método privado para carregar os usuários do arquivo JSON."""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [User.from_dict(item) for item in data]

    def _save(self):
        """Método privado para salvar a lista de usuários em memória no JSON."""
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.users], f, indent=4, ensure_ascii=False)

    def get_all(self):
        """Retorna todos os usuários."""
        return self.users

    def get_by_id(self, user_id: str):
        """Busca e retorna um usuário pelo seu ID."""
        return next((u for u in self.users if u.id == user_id), None)

    def get_by_email(self, email: str):
        """Busca e retorna um usuário pelo seu email."""
        return next((u for u in self.users if u.email.lower() == email.lower()), None)

    def gerar_proximo_id(self):
        """Gera um novo ID de usuário sequencial."""
        if not self.users:
            return "U001"
        ultimo_id = max([int(u.id.replace("U", "")) for u in self.users])
        proximo_num = ultimo_id + 1
        return f"U{proximo_num:03d}"

    def add_user(self, user: User):
        """Adiciona um novo usuário e salva no arquivo."""
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
