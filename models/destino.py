from models.voo import Voo

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
