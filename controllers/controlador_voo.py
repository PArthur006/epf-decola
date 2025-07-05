from datetime import datetime
from .controlador_base import ControladorBase

class ControladorVoo(ControladorBase):
    """
    Controller responsável por todas as rotas relacionadas a voos.
    """
    def __init__(self, app):
        super().__init__(app)
        self.configurar_rotas()

    def configurar_rotas(self):
        """Define as rotas de listagem de voos e seleção de assentos."""
        self.app.route('/', method='GET', callback=self.pagina_inicial)
        self.app.route('/voos', method='GET', callback=self.listar_voos)
        self.app.route('/assentos/<voo_id>', method='GET', callback=self.selecionar_assentos)

    def pagina_inicial(self):
        """Exibe a página inicial com o carrossel de destinos populares."""
        # DADOS DE EXEMPLO para o carrossel
        destinos_populares_exemplo = [
            {'cidade': 'Rio de Janeiro', 'preco': '450,00', 'imagem': '/static/img/RioDeJaneiro.png'},
            {'cidade': 'Fernando de Noronha', 'preco': '1.200,00', 'imagem': '/static/img/FernandoDeNoronha.png'},
            {'cidade': 'Gramado', 'preco': '600,00', 'imagem': '/static/img/Gramado.png'},
            {'cidade': 'São Paulo', 'preco': '300,00', 'imagem': '/static/img/SaoPaulo.png'},
            {'cidade': 'Salvador', 'preco': '400,00', 'imagem': '/static/img/Salvador.png'}
        ]
        
        # Renderiza o template 'pagina_inicial.tpl' com os dados
        return self.renderizar('pagina_inicial', destinos_populares=destinos_populares_exemplo)


    def listar_voos(self):
        """Exibe a página com a lista de voos disponíveis."""
        # DADOS DE EXEMPLO - A estrutura agora corresponde às classes Voo e Destino
        # No futuro, isso será substituído por uma chamada ao VooService
        voos_exemplo = [
            {
                'numero_voo': 'DB101', 'cidade': 'Rio de Janeiro', 'preco': '480,00', 
                'imagem': '/static/img/RioDeJaneiro.png', 'assentos_disp': 22, 
                'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 15, 8, 30)
            },
            {
                'numero_voo': 'DB202', 'cidade': 'Fernando de Noronha', 'preco': '1.200,00', 
                'imagem': '/static/img/FernandoDeNoronha.png', 'assentos_disp': 8, 
                'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 15, 10, 0)
            },
            {
                'numero_voo': 'DB303', 'cidade': 'Gramado', 'preco': '600,00', 
                'imagem': '/static/img/Gramado.png', 'assentos_disp': 15, 
                'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 16, 14, 0)
            }
        ]
        # Renderiza o template 'lista_voos.tpl'
        return self.renderizar('lista_voos', voos=voos_exemplo, titulo="Voos Disponíveis")

    def selecionar_assentos(self, voo_id):
        """Renderiza a página de seleção de assentos para um voo específico."""
        # DADOS DE EXEMPLO - Estrutura em português correspondendo ao template
        aviao_exemplo = {
            'modelo': 'Airbus A320',
            'fileiras': 25,
            'layout': ['A', 'B', 'C', None, 'D', 'E', 'F'], # None para o corredor
            'assentos_ocupados': ['A2', 'C1', 'D5', 'F10', 'B12', 'E12'],
            'fileiras_saida': [10, 11]
        }
        
        print(f"Buscando assentos para o voo ID: {voo_id}")
        # Renderiza o template 'mapa_assentos.tpl'
        return self.renderizar('mapa_assentos', aviao=aviao_exemplo, titulo=f"Selecione seu assento - Voo {voo_id}")