from datetime import datetime
import json
import os

class Pagamento:
    """Representa a entidade de um Pagamento, que está sempre associada a uma Reserva."""
    def __init__(self, id_pagamento, reserva, valor, forma_pagamento, status="Pendente", data_pagamento=None):
        """Construtor da classe Pagamento."""
        self.id_pagamento = id_pagamento
        self.reserva = reserva                     
        self.valor = valor
        self.forma_pagamento = forma_pagamento      
        self.status = status                     
        self.data_pagamento = data_pagamento or datetime.now()

    def __repr__(self):
        """Retorna uma representação textual do objeto."""
        return (f"Pagamento(id_pagamento={self.id_pagamento}, reserva_id='{self.reserva.id_reserva}', "
                f"valor={self.valor}, forma_pagamento='{self.forma_pagamento}', "
                f"status='{self.status}', data_pagamento='{self.data_pagamento}')")

    def confirmar_pagamento(self):
        """Muda o status do pagamento para 'Pago' e notifica a reserva associada."""
        self.status = "Pago"
        self.reserva.pagar(self)

    def cancelar_pagamento(self):
        """Muda o status do pagamento para 'Cancelado' e notifica a reserva."""
        self.status = "Cancelado"
        self.reserva.cancelar()

    def to_dict(self):
        """Converte o objeto Pagamento para um dicionário, para ser salvo em JSON."""
        return {
            'ID': self.id_pagamento,
            'ReservaID': self.reserva.id_reserva,
            'Valor': self.valor,
            'FormaPagamento': self.forma_pagamento,
            'Status': self.status,
            'DataPagamento': self.data_pagamento.isoformat()
        }

    @classmethod
    def from_dict(cls, data, reserva_lookup):
        """Cria uma instância de Pagamento a partir de um dicionário."""
        # Usa a função de lookup para encontrar o objeto Reserva completo pelo ID
        reserva = reserva_lookup(data['ReservaID'])
        return cls(
            id_pagamento=data['ID'],
            reserva=reserva,
            valor=data['Valor'],
            forma_pagamento=data['FormaPagamento'],
            status=data['Status'],
            data_pagamento=datetime.fromisoformat(data['DataPagamento'])
        )

    def atualizar_status(self, novo_status):
        self.status = novo_status

    
   

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class PagamentoModel:
    """Classe DAO responsável pela persistência e acesso aos dados dos pagamentos
    no arquivo `pagamentos.json`."""
    FILE_PATH = os.path.join(DATA_DIR, 'pagamentos.json')

    def __init__(self, reserva_model):
        """Construtor que recebe o ReservaModel para poder encontrar reservas."""
        self.reserva_model = reserva_model  
        self.pagamentos = self._load()

    def _reserva_lookup(self, reserva_id):
        """Função auxiliar para buscar uma reserva pelo seu ID."""
        return self.reserva_model.get_by_id(reserva_id)

    def _load(self):
        """Carrega os pagamentos do JSON e reconstrói a associação com as reservas."""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [
                Pagamento.from_dict(item, self._reserva_lookup)
                for item in data
            ]

    def _save(self):
        """Salva a lista de pagamentos em memória de volta no JSON."""
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.pagamentos], f, ensure_ascii=False, indent=4)

    def gerar_proximo_id(self):
        """Gera um novo ID de pagamento sequencial."""
        if not self.pagamentos:
            return "PG0001"

        ultimos_ids = [
            int(p.id_pagamento.replace("PG", ""))
            for p in self.pagamentos
            if p.id_pagamento.startswith("PG") and p.id_pagamento[2:].isdigit()
        ]
        proximo_num = max(ultimos_ids, default=0) + 1
        return f"PG{proximo_num:04d}"

    def get_all(self):
        """Retorna todos os pagamentos."""
        return self.pagamentos

    def get_by_id(self, id_pagamento):
        """Busca e retorna um pagamento pelo seu ID."""
        return next((p for p in self.pagamentos if p.id_pagamento == id_pagamento), None)

    def add(self, pagamento: Pagamento):
        """Adiciona um novo pagamento, gerando seu ID, e salva no arquivo."""
        pagamento.id_pagamento = self.gerar_proximo_id()
        self.pagamentos.append(pagamento)
        self._save()

    def update(self, pagamento_atualizado: Pagamento):
        for i, p in enumerate(self.pagamentos):
            if p.id_pagamento == pagamento_atualizado.id_pagamento:
                self.pagamentos[i] = pagamento_atualizado
                self._save()
                break

    def delete(self, id_pagamento):
        self.pagamentos = [p for p in self.pagamentos if p.id_pagamento != id_pagamento]
        self._save()