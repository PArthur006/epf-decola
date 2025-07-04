from datetime import datetime
from models.voo import Voo
import json
import os


class Destino(Voo):
    def __init__(self, numero_voo, preco, data_partida, data_chegada, assentos_total,
                 cidade, pais, aeroporto):
        super().__init__(numero_voo, preco, data_partida, data_chegada, assentos_total)
        self.cidade = cidade
        self.pais = pais
        self.aeroporto = aeroporto
    
    def __repr__(self):
        return (f"Destino(numero_voo={self.numero_voo}, preco='{self.preco}', "
                f"data_partida='{self.data_partida}', data_chegada='{self.data_chegada}', "
                f"assentos_total={self.assentos_total}, assentos_disp={self.assentos_disp}, "
                f"cidade='{self.cidade}', pais='{self.pais}', aeroporto='{self.aeroporto}')")
    
    def to_dict(self):
        dados_voo = super().to_dict()
        dados_voo.update({
            'Cidade': self.cidade,
            'País': self.pais,
            'Aeroporto': self.aeroporto
        })
        return dados_voo

    @classmethod
    def from_dict(cls, data):
        return cls(
            numero_voo=data['Número do voo'],
            preco=data['Preço'],
            data_partida=data['Data de partida'],
            data_chegada=data['Data de chegada'],
            assentos_total=data['Número de assentos'],
            cidade=data['Cidade'],
            pais=data['País'],
            aeroporto=data['Aeroporto']
        )

    def atualizar_destino(self, cidade=None, pais=None, aeroporto=None):
        if cidade is not None:
            self.cidade = cidade

        if pais is not None:
            self.pais = pais

        if aeroporto is not None:
            self.aeroporto = aeroporto




DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class DestinoModel:
    FILE_PATH = os.path.join(DATA_DIR, 'destinos.json')

    def __init__(self):
        self.destinos = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Converte strings ISO para datetime
            for item in data:
                item['Data de partida'] = datetime.fromisoformat(item['Data de partida'])
                item['Data de chegada'] = datetime.fromisoformat(item['Data de chegada'])
            return [Destino.from_dict(item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([self._format_dates(d.to_dict()) for d in self.destinos], f, ensure_ascii=False, indent=4)

    def _format_dates(self, data_dict):
        if isinstance(data_dict.get('Data de partida'), datetime):
            data_dict['Data de partida'] = data_dict['Data de partida'].isoformat()
        if isinstance(data_dict.get('Data de chegada'), datetime):
            data_dict['Data de chegada'] = data_dict['Data de chegada'].isoformat()
        return data_dict

    def get_all(self):
        return self.destinos

    def get_by_numero_voo(self, numero_voo):
        return next((d for d in self.destinos if d.numero_voo == numero_voo), None)

    def add(self, destino: Destino):
        self.destinos.append(destino)
        self._save()

    def update(self, destino_atualizado: Destino):
        for i, d in enumerate(self.destinos):
            if d.numero_voo == destino_atualizado.numero_voo:
                self.destinos[i] = destino_atualizado
                self._save()
                break

    def delete(self, numero_voo):
        self.destinos = [d for d in self.destinos if d.numero_voo != numero_voo]
        self._save()
