from bottle import request
from .controlador_base import ControladorBase
from models.user import User
from models.reserva import Reserva
from data.database import get_db

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

    def listar_usuarios(self):
        db = next(get_db())
        usuarios = db.query(User).all()
        return self.renderizar('usuarios', usuarios=usuarios, titulo="Lista de Usuários")

    def adicionar_usuario(self):
        """Lida com a adição de um novo usuário."""
        if request.method == 'GET':
            # Mostra o formulário de adição.
            return self.renderizar('formulario_usuario', usuario=None, acao="/usuarios/adicionar")
        else: # POST
            # TODO: Aqui entrará a chamada para o serviço para salvar o novo usuário.
            print("Formulário de adição recebido. Redirecionando...")
            self.redirecionar('/usuarios')

    def editar_usuario(self, user_id):
        """Lida com a edição de um usuário existente."""
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
