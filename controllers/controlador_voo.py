from .controlador_base import ControladorBase
from models.voo import VooModel

class ControladorVoo(ControladorBase):
    """Controller para gerenciar as rotas de visualização de voos e seleção de assentos."""
    def __init__(self, app, voo_model: VooModel):
        """Recebe a instância da aplicação e o modelo de voo compartilhado."""
        super().__init__(app)
        self.voo_model = voo_model
        self.configurar_rotas()

    def configurar_rotas(self):
        """Configurar as rotas de responsabilidade deste controller."""
        self.app.route('/', method='GET', callback=self.pagina_inicial)
        self.app.route('/voos', method='GET', callback=self.listar_voos)
        self.app.route('/assentos/<id_voo>', method='GET', callback=self.selecionar_assentos)

    def pagina_inicial(self):
        """Define a página inicial como a mesma que lista os voos."""
        return self.listar_voos(template='pagina_inicial')

    def listar_voos(self, template='lista_voos'):
        """Busca todos os voos no modelo e os envia para a view."""
        todos_os_voos = self.voo_model.get_all()
        return self.renderizar(template, voos=todos_os_voos, destinos_populares=todos_os_voos, titulo="Voos Disponíveis")

    def selecionar_assentos(self, id_voo):
        """Busca um voo específico e renderiza o mapa de assentos."""
        voo_especifico = self.voo_model.get_by_numero_voo(id_voo)

        if not voo_especifico:
            return "Voo não encontrado!"

        # A lógica de layout de assentos
        aviao_para_template = {
            'modelo': 'Airbus A320 (Exemplo)',
            'fileiras': 25,
            'layout': ['A', 'B', 'C', None, 'D', 'E', 'F'],
            'assentos_ocupados': voo_especifico.assentos_ocupados,
            'fileiras_saida': [10, 11]
        }

        return self.renderizar('mapa_assentos', voo=voo_especifico, aviao=aviao_para_template, titulo=f"Selecione seu assento - Voo {id_voo}")
