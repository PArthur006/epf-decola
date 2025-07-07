from datetime import datetime
from models.user import User, UserModel
from models.voo import Voo, VooModel
import os
import json


class Reserva:
   """Representa a entidade de uma Reserva. Esta é a classe 'cola' que conecta
   um Usuário a um Voo para um Assento específico."""
   def __init__(self, id_reserva, user: User, voo: Voo, assento, status="Pendente", data_reserva=None):
        """Construtor da classe Reserva."""
        self.id_reserva = id_reserva
        self.user = user          
        self.voo = voo            
        self.assento = assento
        self.status = status
        self.data_reserva = data_reserva or datetime.now()
        self.pagamento = None   

   def pagar(self, pagamento):
        """Associa um pagamento a esta reserva e confirma seu status."""
        self.pagamento = pagamento
        self.status = "Confirmada"

   def cancelar(self):
        """Muda o status da reserva para Cancelada e tenta liberar o assento no Voo."""
        self.status = "Cancelada"
        if self.voo.cancelar_reserva():
            print(f"Assento liberado no voo {self.voo.numero_voo}")

   def to_dict(self):
        """Converte o objeto Reserva para um dicionário,m para ser salvo em JSON."""
        # Salva apenas os IDs das outras entidades para evitar dados aninhados e complexos no JSON.
        return {
            'ID': self.id_reserva,
            'UserID': self.user.id,
            'NumeroVoo': self.voo.numero_voo,
            'Assento': self.assento,
            'Status': self.status,
            'DataReserva': self.data_reserva.isoformat(),
            'PagamentoID': self.pagamento.id_pagamento if self.pagamento else None
        }

   @classmethod
   def from_dict(cls, data, user_lookup, voo_lookup, pagamento_lookup):
        """Cria uma instância de Reserva a partir de um dicionário.
        Usa funções 'lookup' para encontrar e associar os objetos User e Voo completos."""
        user = user_lookup(data['UserID'])
        voo = voo_lookup(data['NumeroVoo'])
        reserva = cls(
            id_reserva=data['ID'],
            user=user,
            voo=voo,
            assento=data['Assento'],
            status=data['Status'],
            data_reserva=datetime.fromisoformat(data['DataReserva'])
        )
        pagamento_id = data.get('PagamentoID')
        # Associa o pagamento depois, para quebrar a dependência circular na criação.
        if pagamento_id:
            reserva.pagamento = pagamento_lookup(pagamento_id)
        return reserva


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class ReservaModel:
    """Classe DAO para gerenciar a persistência e o acesso aos dados de todos todas as reservas."""
    FILE_PATH = os.path.join(DATA_DIR, 'reservas.json')

    def __init__(self, user_model: UserModel, voo_model: VooModel, pagamento_model):
        """Construtor que recebe os outros models como dependências para poder
        conectar as informações ao carregar as reservas."""
        self.user_model = user_model
        self.voo_model = voo_model
        self.pagamento_model = pagamento_model
        self.reservas = self._load()

    def _load(self):
        """Método privado para carregar as reservas do arquivo JSON e
        reconstruir as associações entre Reserva, User e Voo."""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Funções auxiliares para encontrar os objetos com base nos IDs salvos no JSON.
            def user_lookup(uid): return self.user_model.get_by_id(uid)
            def voo_lookup(nv): return self.voo_model.get_by_numero_voo(nv)
            # O lookup de pagamento pode ser nulo se o pagamento_model ainda não foi associado.
            def pagamento_lookup(pid): return self.pagamento_model.get_by_id(pid)

            reservas = []
            for item in data:
                reserva = Reserva.from_dict(item, user_lookup, voo_lookup, pagamento_lookup)
                reservas.append(reserva)

            # Após carregar todas as reservas, associa cada uma ao seu respectivo usuário.
            for r in reservas:
                if r.user:
                    r.user.add_reserva(r)

            return reservas

    def _save(self):
        """Salva a lista de reservas em memória de volta no arquivo JSON."""
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self.reservas], f, indent=4, ensure_ascii=False)

    def get_all(self):
        """Retorna todas as reservas."""
        return self.reservas

    def get_by_id(self, id_reserva):
        """Busca e retorna uma reserva pelo seu ID."""
        return next((r for r in self.reservas if r.id_reserva == id_reserva), None)

    def add(self, reserva: Reserva):
        """Adiciona uma nova reserva e salva no arquivo."""
        self.reservas.append(reserva)
        reserva.user.add_reserva(reserva)
        self._save()

    def update(self, reserva_atualizada: Reserva):
        """Atualiza uma reserva existente."""
        for i, r in enumerate(self.reservas):
            if r.id_reserva == reserva_atualizada.id_reserva:
                self.reservas[i] = reserva_atualizada
                self._save()
                break

    def delete(self, id_reserva):
        """Deleta uma reserva."""
        reserva = self.get_by_id(id_reserva)
        if reserva and reserva.user:
            reserva.user.remove_reserva(id_reserva)
        self.reservas = [r for r in self.reservas if r.id_reserva != id_reserva]
        self._save()
