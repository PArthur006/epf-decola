from datetime import datetime
from .destino import Destino
import json
import os

class Voo:
    """Representa a entidade de um Voo, contendo todas as
    suas informações e o seu Destino associado."""
    def __init__(self, numero_voo, preco, data_partida, data_chegada,
                 assentos_total, comp_aerea, destino: Destino):
        """Construtor da classe Voo."""
        self.numero_voo = numero_voo
        self.preco = preco
        self.data_partida = data_partida
        self.data_chegada = data_chegada
        self.assentos_total = assentos_total
        # A contagem de assentos disponíveis é calculada dinamicamente.
        self.assentos_disp = assentos_total
        # Lista com os identificadores dos assentos já reservados.
        self.assentos_ocupados = []  
        self.comp_aerea = comp_aerea
        # Atributo que armazena o objeto Destino associado a este voo.
        self.destino = destino

    def __repr__(self):
        """Retorna uma representação textual do objeto, para depuração."""
        return (f"Voo(numero_voo={self.numero_voo}, preco={self.preco}, "
                f"data_partida={self.data_partida}, data_chegada={self.data_chegada}, "
                f"assentos_total={self.assentos_total}, assentos_disp={self.assentos_disp}, "
                f"comp_aerea='{self.comp_aerea}', destino={self.destino})")

    def to_dict(self):
        """Converte o objeto Voo para um dicionário, para ser salvo em JSON."""
        return {
            'Número do voo': self.numero_voo,
            'Preço': self.preco,
            'Data de partida': self.data_partida.isoformat(),
            'Data de chegada': self.data_chegada.isoformat(),
            'Número de assentos': self.assentos_total,
            'Assentos disponíveis': self.assentos_disp,
            'Assentos ocupados': self.assentos_ocupados,
            'Companhia Aérea': self.comp_aerea,
            # Converte também o objeto Destino alinhado para um dicionário.
            'Destino': self.destino.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância de Voo a partir de um dicionário"""
        voo = cls(
            numero_voo=data['Número do voo'],
            preco=data['Preço'],
            data_partida=datetime.fromisoformat(data['Data de partida']),
            data_chegada=datetime.fromisoformat(data['Data de chegada']),
            assentos_total=data['Número de assentos'],
            comp_aerea=data['Companhia Aérea'],
            destino=Destino.from_dict(data['Destino'])
        )
        # Carrega os assentos ocupados, se existirem no arquivo.
        voo.assentos_ocupados = data.get('Assentos ocupados', [])
        return voo
    
    def assentos_disponiveis(self):
        """Verifica se ainda há assentos disponíveis neste voo."""
        return self.assentos_disp > 0

    def reservar(self, assento):
        """Tenta reservar um assento específico, atualizando a lista de ocupados."""
        if assento not in self.assentos_ocupados:
            self.assentos_ocupados.append(assento)
            self.assentos_disp -= 1
            return True
        return False

    def cancela_reserva(self, assento):
        """Libera um assento que foi cancelado."""
        if assento in self.assentos_ocupados:
         self.assentos_ocupados.remove(assento)
         self.assentos_disp += 1
         return True
        return False


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class VooModel:
    """Classe responsável pela persistência e acesso aos dados dos voos.
    msnipulando o arquivo 'voos.json'. Funciona como um Data Access Object (DAO)."""
    FILE_PATH = os.path.join(DATA_DIR, 'voos.json')

    def __init__(self):
        """Construtor que carrega todos os voos do JSON para memória."""
        self.voos = self._load()

    def _load(self):
        """Método privado para carregar os voos do arquivo JSON."""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Cria uma lista de objetos Voo a partir dos dados do JSON.
            return [Voo.from_dict(item) for item in data]

    def _save(self):
        """Método privado para salvar a lista de voos em memória de volta no JSON."""
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([v.to_dict() for v in self.voos], f, ensure_ascii=False, indent=4)

    def reload(self):
        """Recarrega os voos do disco para a memória."""
        self.voos = self._load()

    def get_all(self):
      """Retorna todos osvoos, atualizando a contagem de assentos disponíveis."""
      for voo in self.voos:
         voo.assentos_disp = voo.assentos_total - len(voo.assentos_ocupados)
      return self.voos


    def get_by_numero_voo(self, numero_voo):
      """Retorna um voo específico pelo seu número."""
      voo = next((v for v in self.voos if v.numero_voo == numero_voo), None)
      if voo:
         # Garante que a contagem de assentos disponíveis esteja sempre correta.
         voo.assentos_disp = voo.assentos_total - len(voo.assentos_ocupados)
      return voo


    def add(self, voo: Voo):
        """Adiciona um novo voo à lista e salva no arquivo."""
        self.voos.append(voo)
        self._save()

    def update(self, voo_atualizado: Voo):
        """Atualiza um voo existente na lista e salva no arquivo."""
        for i, v in enumerate(self.voos):
            if v.numero_voo == voo_atualizado.numero_voo:
                self.voos[i] = voo_atualizado
                self._save()
                break

    def delete(self, numero_voo):
        """Deleta um voo da lista e salva no arquivo."""
        self.voos = [v for v in self.voos if v.numero_voo != numero_voo]
        self._save()



    
    
