from .base_controller import BaseController

class AuthController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/login', method='GET', callback=self.login_page)
        self.app.route('/signup', method='GET', callback=self.signup_page)

    def login_page(self):
        return self.render('login')
    
    def signup_page(self):
        return self.render('signup')