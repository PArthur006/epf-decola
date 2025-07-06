from datetime import datetime
import os
import json

from models.user import User, UserModel
from models.voo import Voo, VooModel

class Reserva:
   def __init__(self, id_reserva, user: User, voo: Voo, assento, status="Pendente", data_reserva=None):
        self.id_reserva = id_reserva
        self.user = user          # referência para o usuário
        self.voo = voo            # referência para o voo
        self.assento = assento
        self.status = status
        self.data_reserva = data_reserva or datetime.now()
        self.pagamento = None     # referência para pagamento, inicialmente None

   def pagar(self, pagamento):
        self.pagamento = pagamento
        self.status = "Confirmada"

   def cancelar(self):
        self.status = "Cancelada"
        if self.voo.cancelar_reserva():
            print(f"Assento liberado no voo {self.voo.numero_voo}")

   def to_dict(self):
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
        if pagamento_id:
            reserva.pagamento = pagamento_lookup(pagamento_id)
        return reserva


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class ReservaModel:
    FILE_PATH = os.path.join(DATA_DIR, 'reservas.json')

    def __init__(self, user_model: UserModel, voo_model: VooModel, pagamento_model):
        self.user_model = user_model
        self.voo_model = voo_model
        self.pagamento_model = pagamento_model
        self.reservas = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Funções para lookup por id
            def user_lookup(uid): return self.user_model.get_by_id(uid)
            def voo_lookup(nv): return self.voo_model.get_by_numero_voo(nv)
            def pagamento_lookup(pid): return self.pagamento_model.get_by_id(pid)

            reservas = []
            for item in data:
                reserva = Reserva.from_dict(item, user_lookup, voo_lookup, pagamento_lookup)
                reservas.append(reserva)

            # Associar reservas aos usuários
            for r in reservas:
                if r.user:
                    r.user.add_reserva(r)

            return reservas

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self.reservas], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.reservas

    def get_by_id(self, id_reserva):
        return next((r for r in self.reservas if r.id_reserva == id_reserva), None)

    def add(self, reserva: Reserva):
        self.reservas.append(reserva)
        reserva.user.add_reserva(reserva)
        self._save()

    def update(self, reserva_atualizada: Reserva):
        for i, r in enumerate(self.reservas):
            if r.id_reserva == reserva_atualizada.id_reserva:
                self.reservas[i] = reserva_atualizada
                self._save()
                break

    def delete(self, id_reserva):
        reserva = self.get_by_id(id_reserva)
        if reserva and reserva.user:
            reserva.user.remove_reserva(id_reserva)
        self.reservas = [r for r in self.reservas if r.id_reserva != id_reserva]
        self._save()
