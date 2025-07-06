# controllers/__init__.py (VERSÃO FINAL)

from models.user import UserModel
from models.voo import VooModel
from models.destino import DestinoModel
from models.reserva import ReservaModel
from models.pagamento import PagamentoModel

from .controlador_usuario import ControladorUsuario
from .controlador_autenticacao import ControladorAutenticacao
from .controlador_voo import ControladorVoo
from .controlador_pagamento import ControladorPagamento

def init_controllers(app):
    """
    Inicializa todos os models e controllers, injetando as dependências.
    """
    print("-> Inicializando Models...")
    user_model = UserModel()
    destino_model = DestinoModel()
    voo_model = VooModel() 
    # A ordem de inicialização de Reserva e Pagamento é importante
    reserva_model = ReservaModel(user_model, voo_model, None) # PagamentoModel ainda não existe
    pagamento_model = PagamentoModel(reserva_model)
    reserva_model.pagamento_model = pagamento_model # Completa a referência circular

    print("-> Inicializando Controllers...")
    controlador_autenticacao = ControladorAutenticacao(app, user_model)
    controlador_voo = ControladorVoo(app, voo_model)
    # Passa todos os models que o controlador de pagamento precisa
    controlador_pagamento = ControladorPagamento(app, user_model, voo_model, reserva_model, pagamento_model)
    # A inicialização do controlador de usuário pode ser ativada quando necessário
    # controlador_usuario = ControladorUsuario(app, user_model)
    
    print("✅ Controllers inicializados.")