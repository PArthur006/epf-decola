from .controlador_base import ControladorBase

class ControladorAutenticacao(ControladorBase):
    """
    Controller responsável pelas rotas de autenticação (login, cadastro).
    """
    def __init__(self, app):
        super().__init__(app)
        self.configurar_rotas()

    def configurar_rotas(self):
        """Define as rotas de login e cadastro."""
        # Rotas GET para MOSTRAR as páginas
        self.app.route('/login', method='GET', callback=self.pagina_login)
        self.app.route('/cadastro', method='GET', callback=self.pagina_cadastro)

        # Rotas POST para PROCESSAR os formulários
        self.app.route('/login', method='POST', callback=self.efetuar_login)
        self.app.route('/cadastro', method='POST', callback=self.efetuar_cadastro)

    # Renderização das páginas de autenticação
    def pagina_login(self):
        return self.renderizar('login')
    
    def pagina_cadastro(self):
        return self.renderizar('cadastro')
    
    # Processamento dos formulários de autenticação
    def efetuar_login(self):
        # A lógica de autenticação viria aqui
        print("Recebido POST em /login. Redirecionando...")
        return self.redirecionar('/voos')
    
    def efetuar_cadastro(self):
        # A lógica de autenticação viria aqui
        print("Recebido POST em /cadastro. Redirecionando...")
        return self.redirecionar('/voos')