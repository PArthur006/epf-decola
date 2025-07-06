# controllers/controlador_autenticacao.py (VERSÃO FINAL)

from bottle import request, response
from .controlador_base import ControladorBase
from models.user import UserModel, User

class ControladorAutenticacao(ControladorBase):
    def __init__(self, app, user_model: UserModel):
        super().__init__(app)
        self.user_model = user_model
        self.configurar_rotas()

    def configurar_rotas(self):
        self.app.route('/login', method='GET', callback=self.pagina_login)
        self.app.route('/cadastro', method='GET', callback=self.pagina_cadastro)
        self.app.route('/login', method='POST', callback=self.efetuar_login)
        self.app.route('/cadastro', method='POST', callback=self.efetuar_cadastro)
        self.app.route('/logout', method='GET', callback=self.efetuar_logout)

    def pagina_login(self, erro=None):
        return self.renderizar('login', erro=erro)
    
    def pagina_cadastro(self, erro=None):
        return self.renderizar('cadastro', erro=erro)
    
    def efetuar_login(self):
        email = request.forms.get('email')
        senha = request.forms.get('password')
        usuario_encontrado = self.user_model.get_by_email(email)

        if usuario_encontrado and usuario_encontrado.password == senha:
            response.set_cookie("user_id", usuario_encontrado.id, secret='sua-chave-secreta-aqui', path='/')
            return self.redirecionar('/voos')
        else:
            return self.pagina_login(erro='Email ou senha inválidos.')

    def efetuar_cadastro(self):
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('password')
        confirmar_senha = request.forms.get('confirm_password')

        if senha != confirmar_senha:
            return self.pagina_cadastro(erro='As senhas não coincidem.')
        
        if self.user_model.get_by_email(email):
            return self.pagina_cadastro(erro='Este email já está em uso.')

        novo_usuario = User(
            user_id=self.user_model.gerar_proximo_id(),
            name=nome, email=email, password=senha,
            birthdate="N/A", cpf="000.000.000-00", nationality="N/A"
        )
        self.user_model.add_user(novo_usuario)
        return self.redirecionar('/login')

    def efetuar_logout(self):
        """
        Remove o cookie de sessão de forma mais robusta para garantir o logout.
        """
        # --- CORREÇÃO AQUI ---
        # Técnica mais garantida: define o cookie com um valor vazio e
        # uma data de expiração no passado (expires=0), forçando o navegador a deletá-lo.
        response.set_cookie("user_id", "", expires=0, path='/')
        
        # A linha abaixo é uma segurança extra, mas a principal é a de cima.
        response.delete_cookie("user_id", path='/')
        
        # Redireciona o usuário para a página de login.
        return self.redirecionar('/login')