from datetime import datetime
from typing import Optional
import json
import os

class Voo:
    def __init__(self, numero_voo, preco, data_partida, data_chegada, assentos_total):
        self.numero_voo = numero_voo
        self.preco = preco
        self.data_partida = data_partida
        self.data_chegada = data_chegada
        self.assentos_total = assentos_total
        self.assentos_disp = assentos_total
        pass 

    def __repr__(self):
     return (f"Voo(numero_voo={self.numero_voo}, preco='{self.preco}', data_partida='{self.data_partida}', "
            f"data_chegada='{self.data_chegada}', assentos_total={self.assentos_total}, assentos_disp={self.assentos_disp})")

    
    def to_dict(self):
        return{
        'Número do voo': self.numero_voo,
        'Data de partida': self.data_partida,              
        'Data de chegada': self.data_chegada,
        'Número de assentos': self.assentos_total,
        'Preço': self.preco

        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
           numero_voo = data['Número do voo'],
           data_partida = data['Data de partida'],
           data_chegada = data['Data de chegada'],
           assentos_total = data['Número de assentos'],
           preco = data['Preço']
        )
    
    # Assentos
    
    def assentos_disponiveis(self):
        return self.assentos_disp > 0

    def reserva(self):
        if self.assentos_disp > 0:
            self.assentos_disp -= 1
            return True
        return False
    
    def cancel_reserva(self):
        if self.assentos_disp < self.assentos_total:
            self.assentos_disp += 1
            return True
        return False
       
   

    #Inserção de informaçoes
    def definir_dados_voo(self, numero_voo, preco, data_partida, data_chegada, assentos_total):
        self.numero_voo = numero_voo
        self.preco = preco
        self.data_partida = data_partida
        self.data_chegada = data_chegada
        self.assentos_total = assentos_total
        self.assentos_disp = assentos_total

   
    def atualizar_voo( self, preco: Optional[float] = None,data_partida: Optional[datetime] = None,
     data_chegada: Optional[datetime] = None, assentos_total: Optional[int] = None):
        
        if preco is not None:
            if preco < 0:
                raise ValueError("Preço não pode ser negativo.")
            self.preco = preco

        if data_partida is not None:
            self.data_partida = data_partida

        if data_chegada is not None:
            self.data_chegada = data_chegada

        if self.data_partida and self.data_chegada:
            if self.data_chegada < self.data_partida:
                raise ValueError("Data de chegada não pode ser anterior à data de partida.")

        if assentos_total is not None:
            if assentos_total <= 0:
                raise ValueError("Número de assentos deve ser maior que zero.")

            reservas_atuais = self.assentos_total - self.assentos_disp
            if assentos_total < reservas_atuais:
                raise ValueError(
                    f"Não é possível reduzir para {assentos_total} assentos. "
                    f"Já existem {reservas_atuais} reservas feitas."
                )

            diferenca = assentos_total - self.assentos_total
            self.assentos_total = assentos_total
            self.assentos_disp += diferenca

            if self.assentos_disp > self.assentos_total:
                self.assentos_disp = self.assentos_total

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class VooModel:
    FILE_PATH = os.path.join(DATA_DIR, 'voos.json')

    def __init__(self):
        self.voos = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                item['Data de partida'] = datetime.fromisoformat(item['Data de partida'])
                item['Data de chegada'] = datetime.fromisoformat(item['Data de chegada'])
            return [Voo.from_dict(item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([self._format_dates(v.to_dict()) for v in self.voos], f, ensure_ascii=False, indent=4)

    def _format_dates(self, data_dict):
        if isinstance(data_dict.get('Data de partida'), datetime):
            data_dict['Data de partida'] = data_dict['Data de partida'].isoformat()
        if isinstance(data_dict.get('Data de chegada'), datetime):
            data_dict['Data de chegada'] = data_dict['Data de chegada'].isoformat()
        return data_dict

    def get_all(self):
        return self.voos

    def get_by_numero_voo(self, numero_voo):
        return next((v for v in self.voos if v.numero_voo == numero_voo), None)

    def add(self, voo: Voo):
        self.voos.append(voo)
        self._save()

    def update(self, voo_atualizado: Voo):
        for i, v in enumerate(self.voos):
            if v.numero_voo == voo_atualizado.numero_voo:
                self.voos[i] = voo_atualizado
                self._save()
                break

    def delete(self, numero_voo):
        self.voos = [v for v in self.voos if v.numero_voo != numero_voo]
        self._save()  




       