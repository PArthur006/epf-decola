# Importa os models para garantir que o SQLAlchemy possa resolver os relacionamentos
import models

# Importa os controllers que serão inicializados.
from .controlador_autenticacao import ControladorAutenticacao
from .controlador_usuario import ControladorUsuario
from .controlador_voo import ControladorVoo
from .controlador_pagamento import ControladorPagamento

def init_controllers(app):
    """
    Ponto de entrada chamado pelo app.py para inicializar a aplicação.

    Cria as instâncias dos controllers, passando a aplicação.
    """
    
    print("-> Inicializando Controllers...")
    # Cria as instâncias dos controllers, passando a aplicação.
    ControladorAutenticacao(app)
    ControladorUsuario(app)
    ControladorVoo(app)
    ControladorPagamento(app)
    
    print("✅ Controllers inicializados com sucesso.")