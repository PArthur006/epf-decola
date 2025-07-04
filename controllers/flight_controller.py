from .base_controller import BaseController

class FlightController(BaseController):
    """ Responsável por todas as rotas relacionadas a voos. """

    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()

    def setup_routes(self):
            """ Define e registra as rotas na aplicação Bottle. """
            self.app.route('/flights', method='GET', callback=self.list_flights)

    def list_flights(self):
        """ Lista todos os voos disponíveis. """
        """ Implementar a lógica para listar os voos. A lógica a seguir é um exemplo para testes. """

        mock_flights = [
            {
                'id': 1, 'destino': 'Rio de Janeiro', 'preco': '480,00', 'imagem': '/static/img/RioDeJaneiro.png',
                'poltronas_disp': 22, 'companhia': 'Decola-Brasil Airlines', 'embarque': '08:30', 'piloto': 'Alan Turing'
            },
            {
                'id': 2, 'destino': 'Fernando de Noronha', 'preco': '1.200,00', 'imagem': '/static/img/FernandoDeNoronha.png',
                'poltronas_disp': 8, 'companhia': 'Decola-Brasil Airlines', 'embarque': '10:00', 'piloto': 'Grace Hopper'
            },
            {
                'id': 3, 'destino': 'Gramado', 'preco': '600,00', 'imagem': '/static/img/Gramado.png',
                'poltronas_disp': 15, 'companhia': 'Decola-Brasil Airlines', 'embarque': '14:00', 'piloto': 'Mark Zuckerberg'
            },
            {
                'id': 4, 'destino': 'Salvador', 'preco': '550,00', 'imagem': '/static/img/Salvador.png',
                'poltronas_disp': 18, 'companhia': 'Decola-Brasil Airlines', 'embarque': '11:45', 'piloto': 'Ada Lovelace'
            }
        ]

        return self.render('flight_page', flights=mock_flights, title="Voos Disponíveis")
