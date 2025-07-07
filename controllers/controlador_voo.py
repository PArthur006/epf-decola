# controllers/controlador_voo.py (VERSÃO FINAL INTEGRADA)

from .controlador_base import ControladorBase
from models.voo import VooModel # Importa o Model

class ControladorVoo(ControladorBase):
    # 1. Recebe o voo_model como argumento
    def __init__(self, app, voo_model: VooModel):
        super().__init__(app)
        # 2. Armazena a instância compartilhada
        self.voo_model = voo_model
        self.configurar_rotas()

    def configurar_rotas(self):
        self.app.route('/', method='GET', callback=self.pagina_inicial)
        self.app.route('/voos', method='GET', callback=self.listar_voos)
        self.app.route('/assentos/<id_voo>', method='GET', callback=self.selecionar_assentos)

    def pagina_inicial(self):
        """A página inicial agora é a mesma que a de listagem de voos."""
        return self.listar_voos(template='pagina_inicial')

    def listar_voos(self, template='lista_voos'):
        """Busca todos os voos no VooModel e os exibe."""
        # 3. REMOVEMOS os dados de exemplo e usamos o model real
        todos_os_voos = self.voo_model.get_all()
        return self.renderizar(template, voos=todos_os_voos, destinos_populares=todos_os_voos, titulo="Voos Disponíveis")

    def selecionar_assentos(self, id_voo):
        """Busca um voo específico e renderiza o mapa de assentos."""
        # 4. Usa o model real para buscar o voo
        voo_especifico = self.voo_model.get_by_numero_voo(id_voo)

        if not voo_especifico:
            return "Voo não encontrado!"

        # A lógica de layout ainda é um exemplo
        aviao_para_template = {
            'modelo': 'Airbus A320 (Exemplo)',
            'fileiras': 25,
            'layout': ['A', 'B', 'C', None, 'D', 'E', 'F'],
            'assentos_ocupados': voo_especifico.assentos_ocupados,  # <-- AQUI
            'fileiras_saida': [10, 11]
        }

        return self.renderizar('mapa_assentos', voo=voo_especifico, aviao=aviao_para_template, titulo=f"Selecione seu assento - Voo {id_voo}")
