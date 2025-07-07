# Importa as classes de Model que serão usadas pelos controllers.
from models.user import UserModel
from models.voo import VooModel
from models.reserva import ReservaModel
from models.pagamento import PagamentoModel

# Importa os controllers que serão inicializados.
from .controlador_autenticacao import ControladorAutenticacao
from .controlador_usuario import ControladorUsuario
from .controlador_voo import ControladorVoo
from .controlador_pagamento import ControladorPagamento

def init_controllers(app):
    """
    Ponto de entrada chamado pelo app.py para inicializar a aplicação.

    Cria uma instância única de cada model e as injeta nos contrutores dos Controllers, garantindo que todos compartilhem a mesma fonte de dados.
    """
    
    print("-> Inicializando Models...")

    # Cria as instâncias dos models.
    user_model = UserModel()
    voo_model = VooModel()
    reserva_model = ReservaModel(user_model, voo_model, None)
    pagamento_model = PagamentoModel(reserva_model)
    # Completa a referência circular necessária para o funcionamento dos models.
    reserva_model.pagamento_model = pagamento_model

    print("-> Inicializando Controllers e injetando dependências...")
    # Cria as instâncias dos controllers, passando a aplicação e os models necessários.
    ControladorAutenticacao(app, user_model)
    ControladorUsuario(app, user_model, reserva_model)
    ControladorVoo(app, voo_model)
    ControladorPagamento(app, user_model, voo_model, reserva_model, pagamento_model)
    
    print("✅ Controllers inicializados com sucesso.")