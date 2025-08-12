import os

class Config:
    """Classe de configuração para a aplicação, contendo variáveis de ambiente e caminhos."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Configurações do servidor
    HOST = 'localhost'
    PORT = 8080
    DEBUG = True
    RELOADER = True

    # Paths
    TEMPLATE_PATH = os.path.join(BASE_DIR, 'views')
    STATIC_PATH = os.path.join(BASE_DIR, 'static')
    DATA_PATH = os.path.join(BASE_DIR, 'data')

    # Outras configurações
    CHAVE_SECRETA = "sAb6O1jr9KT04YZoFLke"
