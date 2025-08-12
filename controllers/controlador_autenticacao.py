from bottle import request, response
import bcrypt
import uuid # for generating random ids
from .controlador_base import ControladorBase
from models.user import User
from config import Config
from data.database import get_db

class ControladorAutenticacao(ControladorBase):
    """Controller responsável por todas as rotas de autenticação."""
    def __init__(self, app):
        """Construtor que recebe a apicação Bottle."""
        super().__init__(app)
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
        db = next(get_db())
        email = request.forms.get('email')
        senha = request.forms.get('password')
        
        usuario_encontrado = db.query(User).filter(User.email == email).first()

        # Valida se o usuário existe e se a senha corresponde.
        if usuario_encontrado and bcrypt.checkpw(senha.encode('utf-8'), usuario_encontrado.password.encode('utf-8')):
            # Cria um cookie para manter o usuário logado.
            response.set_cookie("user_id", usuario_encontrado.id, secret=Config.CHAVE_SECRETA, path='/')
            # Redireciona para a página de voos após o login bem-sucedido.
            return self.redirecionar('/voos')
        else:
            # Em caso de falha, renderiza a página de login novamente com uma mensagem de erro.
            return self.pagina_login(erro='Email ou senha inválidos.')

    def efetuar_cadastro(self):
        """Processa os dados do formulário de cadastro, cria um novo usuário e o salva."""
        db = next(get_db())
        # Coleta os dados do formulário.
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('password')
        confirmar_senha = request.forms.get('confirm_password')

        # Realiza validações básicas.
        if senha != confirmar_senha:
            return self.pagina_cadastro(erro='As senhas não coincidem.')
        
        if db.query(User).filter(User.email == email).first():
            return self.pagina_cadastro(erro='Este email já está em uso.')

        # Cria uma nova instância do objeto User.
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        novo_usuario = User(
            id=f"U{uuid.uuid4().hex[:4].upper()}", # Generate a random ID
            name=nome, email=email, password=hashed_password,
            # Atribui valores padrão para os campos não obrigatórios.
            birthdate="N/A", cpf=f"000.000.000-00-N{uuid.uuid4().hex[:2]}", nationality="N/A"
        )
        # Adiciona o novo usuário ao "banco de dados" JSON.
        db.add(novo_usuario)
        db.commit()
        # Redireciona para a página de login para que o novo usuário possa entrar.
        return self.redirecionar('/login')

    def efetuar_logout(self):
        """Encerra a sessão do usuário, forçando a exclusão do cookie de autenticação."""
        # Define o cookie com valor vazio e data de expiração no passado para forçar a deleção.
        response.set_cookie("user_id", "", expires=0, path='/')
        response.delete_cookie("user_id", path='/')
        return self.redirecionar('/login')