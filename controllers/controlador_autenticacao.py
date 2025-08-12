from bottle import request, response
import bcrypt
from .controlador_base import ControladorBase
from models.user import UserModel, User

class ControladorAutenticacao(ControladorBase):
    """Controller responsável por todas as rotas de autenticação."""
    def __init__(self, app, user_model: UserModel):
        """Construtor que recebe a apicação Bottle e a instância compartilhada do UserModel."""
        super().__init__(app)
        self.user_model = user_model
        self.configurar_rotas()

    def configurar_rotas(self):
        """Mapeia as URLs de autenticação para seus respectivos métodos."""
        # Rotas para exibir as páginas de formulário.
        self.app.route('/login', method='GET', callback=self.pagina_login)
        self.app.route('/cadastro', method='GET', callback=self.pagina_cadastro)

        # Rotas para processar os dados enviados pelos formulários.
        self.app.route('/login', method='POST', callback=self.efetuar_login)
        self.app.route('/cadastro', method='POST', callback=self.efetuar_cadastro)

        # Rota para deslogar o usuário.
        self.app.route('/logout', method='GET', callback=self.efetuar_logout)

    def pagina_login(self, erro=None):
        """Renderiza a página de login, opcionalmente com uma mensagem de erro."""
        return self.renderizar('login', erro=erro)
    
    def pagina_cadastro(self, erro=None):
        """Renderiza a página de cadastro, opicionalmente com uma mensagem de erro."""
        return self.renderizar('cadastro', erro=erro)
    
    def efetuar_login(self):
        """Processa os dados do formulário de login, valida o usuário e gerencia o cookie de sessão."""
        email = request.forms.get('email')
        senha = request.forms.get('password')
        usuario_encontrado = self.user_model.get_by_email(email)

        # Valida se o usuário existe e se a senha corresponde.
        if usuario_encontrado and bcrypt.checkpw(senha.encode('utf-8'), usuario_encontrado.password.encode('utf-8')):
            # Cria um cookie para manter o usuário logado.
            response.set_cookie("user_id", usuario_encontrado.id, secret='sua-chave-secreta-aqui', path='/')
            # Redireciona para a página de voos após o login bem-sucedido.
            return self.redirecionar('/voos')
        else:
            # Em caso de falha, renderiza a página de login novamente com uma mensagem de erro.
            return self.pagina_login(erro='Email ou senha inválidos.')

    def efetuar_cadastro(self):
        """Processa os dados do formulário de cadastro, cria um novo usuário e o salva."""
        # Coleta os dados do formulário.
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('password')
        confirmar_senha = request.forms.get('confirm_password')

        # Realiza validações básicas.
        if senha != confirmar_senha:
            return self.pagina_cadastro(erro='As senhas não coincidem.')
        
        if self.user_model.get_by_email(email):
            return self.pagina_cadastro(erro='Este email já está em uso.')

        # Cria uma nova instância do objeto User.
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        novo_usuario = User(
            user_id=self.user_model.gerar_proximo_id(),
            name=nome, email=email, password=hashed_password,
            # Atribui valores padrão para os campos não obrigatórios.
            birthdate="N/A", cpf="000.000.000-00", nationality="N/A"
        )
        # Adiciona o novo usuário ao "banco de dados" JSON.
        self.user_model.add_user(novo_usuario)
        # Redireciona para a página de login para que o novo usuário possa entrar.
        return self.redirecionar('/login')

    def efetuar_logout(self):
        """Encerra a sessão do usuário, forçando a exclusão do cookie de autenticação."""
        # Define o cookie com valor vazio e data de expiração no passado para forçar a deleção.
        response.set_cookie("user_id", "", expires=0, path='/')
        response.delete_cookie("user_id", path='/')
        return self.redirecionar('/login')