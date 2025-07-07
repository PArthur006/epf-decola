# controllers/__init__.py (VERSÃO FINAL COM INJEÇÃO DE DEPENDÊNCIA)

# 1. Importa todas as classes de Model e Controller
from models.user import UserModel
from models.voo import VooModel
from models.reserva import ReservaModel
from models.pagamento import PagamentoModel

from .controlador_autenticacao import ControladorAutenticacao
from .controlador_usuario import ControladorUsuario
from .controlador_voo import ControladorVoo
from .controlador_pagamento import ControladorPagamento

def init_controllers(app):
    """
    Inicializa todos os models UMA VEZ e os injeta nos controllers.
    """
    print("-> Inicializando Models (Singleton)...")
    # 2. Cria as instâncias únicas dos models
    user_model = UserModel()
    voo_model = VooModel()
    # A ordem aqui é importante para as dependências
    reserva_model = ReservaModel(user_model, voo_model, None)
    pagamento_model = PagamentoModel(reserva_model)
    reserva_model.pagamento_model = pagamento_model # Completa a referência circular

    print("-> Inicializando Controllers e injetando dependências...")
    # 3. Passa as instâncias dos models para os controllers que precisam delas
    ControladorAutenticacao(app, user_model)
    ControladorUsuario(app, user_model, reserva_model)
    ControladorVoo(app, voo_model)
    ControladorPagamento(app, user_model, voo_model, reserva_model, pagamento_model)
    
    print("✅ Controllers inicializados com sucesso.")