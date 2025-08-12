from bottle import request, response
from .controlador_base import ControladorBase
from models.user import User
from models.reserva import Reserva
from data.database import get_db
import bcrypt
import uuid

class ControladorUsuario(ControladorBase):
    """Controller para gerenciar a área do usuário logado ("Minha Conta")
    e as rotas administrativas de CRUD de usuário."""
    def __init__(self, app):
        """Recebe as instâncias compartilhadas dos models de usuários e reserva."""
        super().__init__(app)
        self.configurar_rotas()

    def configurar_rotas(self):
        """Mapeia as URLs de usuário para os métodos correspondentes."""
        self.app.route('/usuarios', method='GET', callback=self.listar_usuarios)
        self.app.route('/usuarios/adicionar', method=['GET', 'POST'], callback=self.adicionar_usuario)
        self.app.route('/usuarios/editar/<user_id>', method=['GET', 'POST'], callback=self.editar_usuario)
        self.app.route('/usuarios/deletar/<user_id>', method='POST', callback=self.deletar_usuario)
        # Rota para a página da conta do usuário logado
        self.app.route('/minha-conta', method='GET', callback=self.pagina_minha_conta)
        self.app.route('/minha-conta/editar', method='POST', callback=self.editar_minha_conta)


    def listar_usuarios(self):
        """Exibe a lista de todos os usuários cadastrados no sistema."""
        db = next(get_db())
        usuarios = db.query(User).all()
        return self.renderizar('usuarios', usuarios=usuarios, titulo="Lista de Usuários")

    def adicionar_usuario(self):
        """Lida com a adição de um novo usuário.

        Se o método da requisição for GET, exibe o formulário de cadastro.
        Se for POST, processa os dados do formulário para criar um novo usuário,
        incluindo validação de CPF, e-mail e hash de senha.
        """
        db = next(get_db())
        if request.method == 'GET':
            # Mostra o formulário de adição.
            return self.renderizar('cadastro', usuario=None, acao="/usuarios/adicionar")
        else: # POST
            name = request.forms.get('name')
            email = request.forms.get('email')
            password = request.forms.get('password')
            birthdate = request.forms.get('birthdate')
            cpf = request.forms.get('cpf')
            nationality = request.forms.get('nationality')
            phone = request.forms.get('phone')

            # Validação de CPF
            if not User.validar_cpf(cpf):
                return self.renderizar('cadastro', erro="CPF inválido.")

            # Verifica se o email já está em uso
            if db.query(User).filter(User.email == email).first():
                return self.renderizar('cadastro', erro="Este email já está em uso.")
            
            # Verifica se o CPF já está em uso
            if db.query(User).filter(User.cpf == cpf).first():
                return self.renderizar('cadastro', erro="Este CPF já está em uso.")

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            new_user = User(
                id=str(uuid.uuid4()),
                name=name,
                email=email,
                password=hashed_password,
                birthdate=birthdate,
                cpf=cpf,
                nationality=nationality,
                phone=phone
            )
            db.add(new_user)
            db.commit()
            self.redirecionar('/login')

    def editar_usuario(self, user_id):
        """Lida com a edição de um usuário existente.

        Esta função é um placeholder. Em uma implementação completa,
        deveria buscar o usuário pelo `user_id` no banco de dados,
        preencher o formulário com seus dados e processar as atualizações.
        """
        # TODO: Aqui entrará a chamada para o serviço para buscar o usuário pelo ID.
        
        # Por enquanto, usamos um dicionário vazio como dado de exemplo.
        usuario_exemplo = {'id': user_id, 'name': 'Usuário de Teste', 'email': 'teste@email.com'}
        
        if not usuario_exemplo: # A verificação continuará funcionando
            return "Usuário não encontrado"

        if request.method == 'GET':
            # Mostra o formulário preenchido com os dados do usuário.
            return self.renderizar('formulario_usuario', usuario=usuario_exemplo, acao=f"/usuarios/editar/{user_id}")
        else: # POST
            # TODO: Aqui entrará a chamada para o serviço para salvar as alterações.
            print(f"Formulário de edição para o usuário {user_id} recebido. Redirecionando...")
            self.redirecionar('/usuarios')

    def deletar_usuario(self, user_id):
        """Lida com a exclusão de um usuário existente.

        Esta função é um placeholder. Em uma implementação completa,
        deveria buscar o usuário pelo `user_id` no banco de dados e excluí-lo.
        """
        # TODO: Aqui entrará a chamada para o serviço para deletar o usuário.
        print(f"Requisição para deletar o usuário {user_id} recebida. Redirecionando...")
        self.redirecionar('/usuarios')

    def pagina_minha_conta(self):
        """Exibe a página de perfil do usuário com seus dados e histórico de reservas."""
        db = next(get_db())
        # Obtém o ID do usuário a partir do cookie de sessão.
        id_usuario_logado = self.obter_usuario_logado()

        # Se não houver usuário logado, redireciona para a tela de login.
        if not id_usuario_logado:
            return self.redirecionar('/login')

        # Busca o objeto completo do usuário usando o ID.
        usuario = db.query(User).filter(User.id == id_usuario_logado).first()
        
        # Caso o cookie exista ma so usuário tenha sido deletado.
        if not usuario:
            return self.redirecionar('/logout')

        # Busca todas as reservas e filtra apenas as que pertencem a este usuário.
        reservas_do_usuario = db.query(Reserva).filter(Reserva.user_id == id_usuario_logado).all()

        # Renderiza o template, passando os dados do usuário e sua lista de reservas.
        return self.renderizar('minha_conta', usuario=usuario, reservas=reservas_do_usuario, titulo="Minha Conta")

    def editar_minha_conta(self):
        """Processa a edição dos dados do perfil do usuário logado."""
        db = next(get_db())
        id_usuario_logado = self.obter_usuario_logado()
        if not id_usuario_logado:
            return self.redirecionar('/login')

        usuario = db.query(User).filter(User.id == id_usuario_logado).first()
        if not usuario:
            return self.redirecionar('/logout')

        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('password')
        confirmar_senha = request.forms.get('confirm_password')

        # Validações
        if senha and senha != confirmar_senha:
            return self.renderizar('minha_conta', usuario=usuario, reservas=usuario.reservas, titulo="Minha Conta", erro="As senhas não coincidem.")
        
        # Verifica se o email já está em uso por outro usuário
        if email != usuario.email and db.query(User).filter(User.email == email).first():
            return self.renderizar('minha_conta', usuario=usuario, reservas=usuario.reservas, titulo="Minha Conta", erro="Este email já está em uso por outro usuário.")

        # Atualiza os dados
        usuario.name = nome
        usuario.email = email
        usuario.birthdate = request.forms.get('birthdate')
        usuario.nationality = request.forms.get('nationality')
        usuario.phone = request.forms.get('phone')

        new_cpf = request.forms.get('cpf')
        if new_cpf and new_cpf != usuario.cpf:
            if not User.validar_cpf(new_cpf):
                return self.renderizar('minha_conta', usuario=usuario, reservas=usuario.reservas, titulo="Minha Conta", erro="CPF inválido.")
            if db.query(User).filter(User.cpf == new_cpf).first():
                return self.renderizar('minha_conta', usuario=usuario, reservas=usuario.reservas, titulo="Minha Conta", erro="Este CPF já está em uso por outro usuário.")
            usuario.cpf = new_cpf

        if senha:
            usuario.password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        db.add(usuario)
        db.commit()

        return self.redirecionar('/minha-conta')