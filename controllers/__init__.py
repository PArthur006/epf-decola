from .controlador_usuario import ControladorUsuario
from .controlador_autenticacao import ControladorAutenticacao
from .controlador_voo import ControladorVoo
from .controlador_pagamento import ControladorPagamento

def init_controllers(app):
    """
    Inicializa todos os controllers, passando a instância da aplicação Bottle.
    Esta função é chamada uma vez quando a aplicação inicia.
    """
    print("-> Inicializando controllers...")
    
    # Cria uma instância de cada controller, registrando suas rotas na aplicação
    controlador_usuario = ControladorUsuario(app)
    controlador_autenticacao = ControladorAutenticacao(app)
    controlador_voo = ControladorVoo(app)
    controlador_pagamento = ControladorPagamento(app)
    
    print("✅ Controllers inicializados.")