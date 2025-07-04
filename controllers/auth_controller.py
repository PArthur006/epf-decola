from .base_controller import BaseController

class AuthController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()

    def setup_routes(self):
        # Rotas GET para visualizar as páginas de login e signup
        self.app.route('/login', method='GET', callback=self.login_page)
        self.app.route('/signup', method='GET', callback=self.signup_page)

        # Rotas POST para processar os formulários de login e signup
        self.app.route('/login', method='POST', callback=self.do_login)
        self.app.route('/signup', method='POST', callback=self.do_signup)

    def login_page(self):
        return self.render('login')
    
    def signup_page(self):
        return self.render('signup')
    
    def do_login(self):
        # Aqui vem a lógica de valoidação do login. Por enquanto, só será redirecionado para a página de voos.
        return self.redirect('/flights')
    
    def do_signup(self):
        # Aqui vem a lógica de validação do signup. Por enquanto, só será redirecionado para a página de voos.
        return self.redirect('/flights')