from bottle import request
from models.reserva import ReservaModel
from .controlador_base import ControladorBase
from models.user import UserModel, User

class ControladorUsuario(ControladorBase):

    def __init__(self, app, reserva_model: ReservaModel):
        super().__init__(app)
        self.configurar_rotas()
        self.user_model = UserModel()
        self.reserva_model = reserva_model

    def configurar_rotas(self):
        """Define as rotas de CRUD de usuário."""
        self.app.route('/usuarios', method='GET', callback=self.listar_usuarios)
        self.app.route('/usuarios/adicionar', method=['GET', 'POST'], callback=self.adicionar_usuario)
        self.app.route('/usuarios/editar/<id_usuario>', method=['GET', 'POST'], callback=self.editar_usuario)
        self.app.route('/usuarios/deletar/<id_usuario>', method='POST', callback=self.deletar_usuario)
        self.app.route('/minha-conta', method='GET', callback=self.pagina_minha_conta) #rota para a página da conta do usuário logado

    def listar_usuarios(self):
        usuarios = self.user_model.get_all()
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

    def editar_usuario(self, id_usuario):
        """Lida com a edição de um usuário existente."""
        # TODO: Aqui entrará a chamada para o serviço para buscar o usuário pelo ID.
        
        # Por enquanto, usamos um dicionário vazio como dado de exemplo.
        usuario_exemplo = {'id': id_usuario, 'name': 'Usuário de Teste', 'email': 'teste@email.com'}
        
        if not usuario_exemplo: # A verificação continuará funcionando
            return "Usuário não encontrado"

        if request.method == 'GET':
            # Mostra o formulário preenchido com os dados do usuário.
            return self.renderizar('formulario_usuario', usuario=usuario_exemplo, acao=f"/usuarios/editar/{id_usuario}")
        else: # POST
            # TODO: Aqui entrará a chamada para o serviço para salvar as alterações.
            print(f"Formulário de edição para o usuário {id_usuario} recebido. Redirecionando...")
            self.redirecionar('/usuarios')

    def deletar_usuario(self, id_usuario):
        # TODO: Aqui entrará a chamada para o serviço para deletar o usuário.
        print(f"Requisição para deletar o usuário {id_usuario} recebida. Redirecionando...")
        self.redirecionar('/usuarios')

    def pagina_minha_conta(self):
        """Exibe a página de perfil do usuário com seus dados e reservas."""
        id_usuario_logado = self.obter_usuario_logado()
        if not id_usuario_logado:
            return self.redirecionar('/login')

        usuario = self.user_model.get_by_id(id_usuario_logado)
        if not usuario:
            return self.redirecionar('/logout')

        # --- LÓGICA CORRIGIDA AQUI ---
        # 1. Pega TODAS as reservas que existem no sistema.
        todas_as_reservas = self.reserva_model.get_all()
        
        # 2. Filtra a lista, pegando apenas as reservas cujo ID do usuário
        #    é o mesmo do usuário que está logado.
        reservas_do_usuario = [r for r in todas_as_reservas if r.user and r.user.id == id_usuario_logado]

        # 3. Envia para o template o objeto 'usuario' e a lista de 'reservas' separadamente.
        return self.renderizar('minha_conta', usuario=usuario, reservas=reservas_do_usuario, titulo="Minha Conta")