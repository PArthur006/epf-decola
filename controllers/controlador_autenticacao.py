from .controlador_base import ControladorBase

class ControladorAutenticacao(ControladorBase):
    """
    Controller responsável pelas rotas de autenticação (login, cadastro).
    """
    def __init__(self, app):
        # Inicializa a classe pai
        super().__init__(app)
        # Configura as rotas deste controller
        self.configurar_rotas()

    def configurar_rotas(self):
        """Define as rotas de login e cadastro."""
        # Rotas GET para MOSTRAR as páginas
        self.app.route('/login', method='GET', callback=self.pagina_login)
        self.app.route('/cadastro', method='GET', callback=self.pagina_cadastro) # Rota corrigida

        # Rotas POST para PROCESSAR os formulários
        self.app.route('/login', method='POST', callback=self.efetuar_login)
        self.app.route('/cadastro', method='POST', callback=self.efetuar_cadastro) # Rota corrigida

    def pagina_login(self):
        """Renderiza a página de login."""
        return self.renderizar('login')
    
    def pagina_cadastro(self):
        """Renderiza a página de cadastro."""
        return self.renderizar('cadastro')
    
    def efetuar_login(self):
        """Processa o login e redireciona. (Lógica de validação virá depois)"""
        print("Recebido POST em /login. Redirecionando...")
        return self.redirecionar('/voos')
    
    def efetuar_cadastro(self):
        """Processa o cadastro e redireciona. (Lógica de criação de usuário virá depois)"""
        print("Recebido POST em /cadastro. Redirecionando...")
        return self.redirecionar('/voos')