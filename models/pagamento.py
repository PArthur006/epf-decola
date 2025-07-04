from datetime import datetime
import json
import os

class Pagamento:
    def __init__(self, id_pagamento, numero_voo, valor, forma_pagamento, status, data_pagamento=None):
        self.id_pagamento = id_pagamento
        self.numero_voo = numero_voo
        self.valor = valor
        self.forma_pagamento = forma_pagamento  # Ex: 'Cartão', 'PIX', 'Boleto'
        self.status = status                    # Ex: 'Pendente', 'Pago', 'Cancelado'
        self.data_pagamento = data_pagamento or datetime.now()

    def __repr__(self):
        return (f"Pagamento(id_pagamento={self.id_pagamento}, numero_voo='{self.numero_voo}', "
                f"valor={self.valor}, forma_pagamento='{self.forma_pagamento}', "
                f"status='{self.status}', data_pagamento='{self.data_pagamento}')")
    
    def to_dict(self):
        return {
            'ID': self.id_pagamento,
            'Número do voo': self.numero_voo,
            'Valor': self.valor,
            'Forma de pagamento': self.forma_pagamento,
            'Status': self.status,
            'Data do pagamento': self.data_pagamento.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_pagamento=data['ID'],
            numero_voo=data['Número do voo'],
            valor=data['Valor'],
            forma_pagamento=data['Forma de pagamento'],
            status=data['Status'],
            data_pagamento=datetime.fromisoformat(data['Data do pagamento'])
        )

    def atualizar_status(self, novo_status):
        self.status = novo_status

    
   

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class PagamentoModel:
    FILE_PATH = os.path.join(DATA_DIR, 'pagamentos.json')

    def __init__(self):
        self.pagamentos = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                item['Data do pagamento'] = datetime.fromisoformat(item['Data do pagamento'])
            return [Pagamento.from_dict(item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([self._format_dates(p.to_dict()) for p in self.pagamentos], f, ensure_ascii=False, indent=4)

    def _format_dates(self, data_dict):
        if isinstance(data_dict.get('Data do pagamento'), datetime):
            data_dict['Data do pagamento'] = data_dict['Data do pagamento'].isoformat()
        return data_dict

    def gerar_proximo_id(self):
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
        return self.pagamentos

    def get_by_id(self, id_pagamento):
        return next((p for p in self.pagamentos if p.id_pagamento == id_pagamento), None)

    def add(self, pagamento: Pagamento):
        # Sempre gera um novo ID automaticamente ao adicionar
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