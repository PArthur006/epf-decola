from datetime import datetime
import json
import os
from .destino import Destino

class Voo:
    def __init__(self, numero_voo, preco, data_partida, data_chegada,
                 assentos_total, comp_aerea, destino: Destino):
        self.numero_voo = numero_voo
        self.preco = preco
        self.data_partida = data_partida
        self.data_chegada = data_chegada
        self.assentos_total = assentos_total
        self.assentos_disp = assentos_total
        self.assentos_ocupados = []  # lista de assentos já reservados
        self.comp_aerea = comp_aerea
        self.destino = destino

    def __repr__(self):
        return (f"Voo(numero_voo={self.numero_voo}, preco={self.preco}, "
                f"data_partida={self.data_partida}, data_chegada={self.data_chegada}, "
                f"assentos_total={self.assentos_total}, assentos_disp={self.assentos_disp}, "
                f"comp_aerea='{self.comp_aerea}', destino={self.destino})")

    def to_dict(self):
        return {
            'Número do voo': self.numero_voo,
            'Preço': self.preco,
            'Data de partida': self.data_partida.isoformat(),
            'Data de chegada': self.data_chegada.isoformat(),
            'Número de assentos': self.assentos_total,
            'Assentos disponíveis': self.assentos_disp,
            'Assentos ocupados': self.assentos_ocupados,
            'Companhia Aérea': self.comp_aerea,
            'Destino': self.destino.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        voo = cls(
            numero_voo=data['Número do voo'],
            preco=data['Preço'],
            data_partida=datetime.fromisoformat(data['Data de partida']),
            data_chegada=datetime.fromisoformat(data['Data de chegada']),
            assentos_total=data['Número de assentos'],
            comp_aerea=data['Companhia Aérea'],
            destino=Destino.from_dict(data['Destino'])
        )
        voo.assentos_ocupados = data.get('Assentos ocupados', [])
        return voo
    
    def assentos_disponiveis(self):
        return self.assentos_disp > 0

    def reservar(self, assento):
        if assento not in self.assentos_ocupados:
            self.assentos_ocupados.append(assento)
            self.assentos_disp -= 1
            return True
        return False

    def cancela_reserva(self, assento):
        if assento in self.assentos_ocupados:
         self.assentos_ocupados.remove(assento)
         self.assentos_disp += 1
         return True
        return False


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
            # A conversão de data foi REMOVIDA daqui.
            # Agora, apenas passamos os dados brutos do JSON para o Voo.from_dict
            return [Voo.from_dict(item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([v.to_dict() for v in self.voos], f, ensure_ascii=False, indent=4)

    def reload(self):
        """Recarrega os voos a partir do arquivo JSON no disco."""
        self.voos = self._load()

    def get_all(self):
      """
      Retorna todos os voos, atualizando o número de assentos disponíveis
      com base nos assentos ocupados.
      """
      for voo in self.voos:
         voo.assentos_disp = voo.assentos_total - len(voo.assentos_ocupados)
      return self.voos


    def get_by_numero_voo(self, numero_voo):
      """
      Retorna o voo correspondente ao número especificado,
      atualizando também o número de assentos disponíveis.
      """
      voo = next((v for v in self.voos if v.numero_voo == numero_voo), None)
      if voo:
         voo.assentos_disp = voo.assentos_total - len(voo.assentos_ocupados)
      return voo


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



    
    
