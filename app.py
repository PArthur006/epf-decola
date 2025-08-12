from bottle import Bottle
from config import Config

class App:
    """Classe principal da aplicação que configura e executa o servidor Bottle."""
    def __init__(self):
        """Inicializa a aplicação Bottle e carrega as configurações."""
        self.bottle = Bottle()
        self.config = Config()

    def setup_routes(self):
        """Configura as rotas da aplicação importando e inicializando os controladores."""
        from controllers import init_controllers

        print('🚀 Inicializa rotas!')
        init_controllers(self.bottle)

    def run(self):
        """Inicia o servidor Bottle com as configurações definidas."""
        self.setup_routes()
        self.bottle.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEBUG,
            reloader=self.config.RELOADER
        )

def create_app():
    """Função de fábrica para criar uma instância da aplicação."""
    return App()
