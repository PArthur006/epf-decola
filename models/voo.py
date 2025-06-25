class Voo:
    def __init__(self, numero_voo, preco, data_partida, data_chegada, assentos):
        self.numero_voo = numero_voo
        self.preco = preco
        self.data_partida = data_partida
        self.data_chegada = data_chegada
        self.assentos = assentos
        pass 

    def __repr__(self):
        return(f"Numero do voo(numero_voo={self.numero_voo}, preco='{self.preco}', data de partida='{self.data_partida}', "
                f"data de chegada='{self.data_chegada}', assentos'{self.assentos}'")
    
    def to_dict(self):
        return{
        'Número do voo': self.numero_voo,
        'Data de partida': self.data_partida,              
        'Data de chegada': self.data_chegada,
        'Número de assentos': self.assentos,
        'Preço': self.preco

        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
           numero_voo = data['Número do voo'],
           data_partida = data['Data de partida'],
           data_chegada = data['Data de chegada'],
           assentos = data['Número de assentos'],
           preco = data['Preço']
        )
    

    
