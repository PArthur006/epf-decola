from datetime import datetime
from .controlador_base import ControladorBase
from types import SimpleNamespace

DADOS_VOOS = {

    'DB101': {

        'cidade': 'Rio de Janeiro', 'preco': '480,00', 'imagem': '/static/img/RioDeJaneiro.png',

        'assentos_total': 150, 'assentos_ocupados': ['A2', 'C1', 'D5', 'F10'], 

        'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 15, 8, 30)

    },

    'DB202': {

        'cidade': 'Fernando de Noronha', 'preco': '1.200,00', 'imagem': '/static/img/FernandoDeNoronha.png',

        'assentos_total': 120, 'assentos_ocupados': ['A1', 'A2', 'A10', 'C14', 'D25'],

        'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 15, 10, 0)

    },

    'DB303': {

        'cidade': 'Gramado', 'preco': '600,00', 'imagem': '/static/img/Gramado.png',

        'assentos_total': 150, 'assentos_ocupados': ['F1', 'F2', 'E3', 'D4', 'C5', 'B6', 'A7'],

        'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 16, 14, 0)

    },

    'DB404': {

        'cidade': 'São Paulo', 'preco': '350,00', 'imagem': '/static/img/SaoPaulo.png',

        'assentos_total': 180, 'assentos_ocupados': [],

        'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 16, 16, 30)

    },

    'DB505': {

        'cidade': 'Salvador', 'preco': '400,00', 'imagem': '/static/img/Salvador.png',

        'assentos_total': 200, 'assentos_ocupados': ['A1', 'B2', 'C3', 'D4', 'E5', 'F6'],

        'comp_aerea': 'Decola-BR', 'data_partida': datetime(2025, 8, 17, 9, 0)

    }

}


class ControladorVoo(ControladorBase):
    def __init__(self, app):
        super().__init__(app)
        self.configurar_rotas()

    def configurar_rotas(self):
        self.app.route('/', method='GET', callback=self.pagina_inicial)
        self.app.route('/voos', method='GET', callback=self.listar_voos)
        self.app.route('/assentos/<id_voo>', method='GET', callback=self.selecionar_assentos)

    def pagina_inicial(self):
        destinos_formatados = []
        for id_voo, dados in DADOS_VOOS.items():
            destino = dados.copy()
            destino['id'] = id_voo
            destinos_formatados.append(SimpleNamespace(**destino))
        return self.renderizar('pagina_inicial', destinos_populares=destinos_formatados)

    def listar_voos(self):
        voos_preparados = []
        for id_voo, dados in DADOS_VOOS.items():
            assentos_disp = dados['assentos_total'] - len(dados['assentos_ocupados'])
            voo_com_id = dados.copy()
            voo_com_id['numero_voo'] = id_voo
            voo_com_id['assentos_disp'] = assentos_disp
            voo_objeto = SimpleNamespace(**voo_com_id)
            voos_preparados.append(voo_objeto)
        return self.renderizar('lista_voos', voos=voos_preparados, titulo="Voos Disponíveis")

    def selecionar_assentos(self, id_voo):
        # Usa o id_voo da URL para pegar os dados do voo correto
        dados_voo = DADOS_VOOS.get(id_voo)

        if not dados_voo:
            return "Voo não encontrado!"

        # Usa a lista de 'assentos_ocupados' específica daquele voo
        aviao_para_template = {
            'modelo': 'Airbus A320 (Exemplo)',
            'fileiras': 25,
            'layout': ['A', 'B', 'C', None, 'D', 'E', 'F'],
            'assentos_ocupados': dados_voo['assentos_ocupados'],
            'fileiras_saida': [10, 11]
        }
        
        return self.renderizar('mapa_assentos', aviao=aviao_para_template, titulo=f"Selecione seu assento - Voo {id_voo}")