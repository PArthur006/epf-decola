from .controlador_base import ControladorBase
from .controlador_voo import DADOS_VOOS

class ControladorPagamento(ControladorBase):
    def __init__(self, app):
        super().__init__(app)
        self.configurar_rotas()

    def configurar_rotas(self):
        self.app.route('/pagamento/<id_voo>/<assentos_selecionados>', method='GET', callback=self.pagina_pagamento)

    def pagina_pagamento(self, id_voo, assentos_selecionados):
        # Busca os dados do voo específico usando o id_voo da URL
        dados_voo = DADOS_VOOS.get(id_voo)
        if not dados_voo:
            return "Voo não encontrado!"

        lista_de_assentos = assentos_selecionados.split(',')
        
        # Monta a reserva com os dados dinâmicos do voo encontrado
        reserva_exemplo = {
            'voo': {
                'id': id_voo,
                'cidade_origem': 'Brasília', # Origem fixa por enquanto
                'cidade_destino': dados_voo['cidade'],
                'data_partida': dados_voo['data_partida'].strftime('%d/%m/%Y'),
                'horario_embarque': dados_voo['data_partida'].strftime('%H:%M')
            },
            'assentos': lista_de_assentos,
            'custo': {
                'valor_por_assento': float(dados_voo['preco'].replace(',', '.')),
                'total': float(dados_voo['preco'].replace(',', '.')) * len(lista_de_assentos)
            }
        }
        
        return self.renderizar('pagamento', reserva=reserva_exemplo, titulo="Pagamento")