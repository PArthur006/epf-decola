from datetime import datetime
import json
import os

class Destino:
    """Representa a entidade de um Destino, com informações sobre
    a cidade, país, aeroporto e uma imagem representativa."""    
    def __init__(self, cidade, pais, aeroporto, imagem):
        """Construtor da classe Destino"""
        self.cidade = cidade
        self.pais = pais
        self.aeroporto = aeroporto
        self.imagem = imagem 

    def __repr__(self):
        """Retorna uma representação textual do objeto."""
        return f"Destino(cidade='{self.cidade}', pais='{self.pais}', imagem='{self.imagem}')"


    def to_dict(self):
        """Converte o objeto Destino para um dicionário, para ser salvo em JSON."""
        return {
            'Cidade': self.cidade,
            'País': self.pais,
            'Aeroporto': self.aeroporto,
            'Imagem': self.imagem
        }

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância de Destino a partir de um dicionário."""
        return cls(
            cidade=data['Cidade'],
            pais=data['País'],
            aeroporto=data['Aeroporto'],
            imagem=data['Imagem']
        )

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
            return [Destino.from_dict(item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([d.to_dict() for d in self.destinos], f, ensure_ascii=False, indent=4)

    def get_all(self):
        return self.destinos

    def add(self, destino: Destino):
        self.destinos.append(destino)
        self._save()

    def update(self, destino_atualizado: Destino):
        for i, d in enumerate(self.destinos):
            if d.cidade == destino_atualizado.cidade and d.pais == destino_atualizado.pais:
                self.destinos[i] = destino_atualizado
                self._save()
                break

    def delete(self, cidade, pais):
        self.destinos = [d for d in self.destinos if not (d.cidade == cidade and d.pais == pais)]
        self._save()
