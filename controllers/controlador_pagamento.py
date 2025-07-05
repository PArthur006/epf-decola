from.controlador_base import ControladorBase

class ControladorPagamento(ControladorBase):
    # Controller responsável pelo fluxo de pagamento.

    def __init__(self, app):
        super().__init__(app)
        self.configurar_rotas()

    def configurar_rotas(self):
        self.app.route('/pagamento/<id_voo>/<assentos_selecionados>', methods='GET', callback=self.pagina_pagamento)

    def pagina_pagamento(self, id_voo, assentos_selecionados):
        # Dados de exemplo que simulam uma reserva completa
        reserva_exemplo = {
            'voo': {
                'id': id_voo,
                'cidade_origem': 'Brasília',
                'cidade_destino': 'Rio de Janeiro',
                'data_partida': '15/08/2025',
                'horario_embarque': '08:30'
            },
            'assentos': assentos_selecionados.split(','), # transforma a string em uma lista
            'custo': {
                'valor_por_assento': 480.00,
                'total': 480.00 * len(assentos_selecionados.split(','))
            }
        }

        return self.renderizar('pagamento', reserva=reserva_exemplo, titulo="Pagamento")