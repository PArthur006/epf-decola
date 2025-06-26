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
     return(f"Voo(numero_voo={self.numero_voo}, preco='{self.preco}', data_partida='{self.data_partida}', "
            f"data_chegada='{self.data_chegada}', assentos_total={self.assentos_total}, assentos_disp={self.assentos_disp}")

    
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
        if self.assentos_disp == 0 :
            print('Não existem assentos disponiveís'),
        else:
            print('Ainda há {self.assentos_disp} assentos disponiveís'),
        pass
    
    def reserva(self,assentos_disp):
        resposta = input('deseja reservar o assento?(sim/não)')
        if resposta == 'sim':
            if assentos_disp > 0:
                assentos_disp -= 1
            else:
             print('invalido') #ver relações com def assentos disponiveis e fazer tratamento de erro
            return assentos_disp
        pass
