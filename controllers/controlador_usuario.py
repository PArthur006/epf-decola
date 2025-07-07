from bottle import request
from .controlador_base import ControladorBase
from models.user import UserModel
from models.reserva import ReservaModel

class ControladorUsuario(ControladorBase):
    # 1. O __init__ agora recebe os models como argumentos
    def __init__(self, app, user_model: UserModel, reserva_model: ReservaModel):
        super().__init__(app)
        # 2. Armazena as instâncias compartilhadas
        self.user_model = user_model
        self.reserva_model = reserva_model
        self.configurar_rotas()

    def configurar_rotas(self):
        """Define as rotas de CRUD de usuário."""
        self.app.route('/usuarios', method='GET', callback=self.listar_usuarios)
        self.app.route('/usuarios/adicionar', method=['GET', 'POST'], callback=self.adicionar_usuario)
        self.app.route('/usuarios/editar/<user_id>', method=['GET', 'POST'], callback=self.editar_usuario)
        self.app.route('/usuarios/deletar/<user_id>', method='POST', callback=self.deletar_usuario)
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
        """Exibe a página de perfil do usuário com seus dados e reservas."""
        # 1. Espião para ver o que está no cookie
        id_usuario_logado = self.obter_usuario_logado()
        print(f"DEBUG MINHA CONTA: Tentando carregar página. Cookie 'user_id' encontrado: '{id_usuario_logado}'")

        if not id_usuario_logado:
            print("DEBUG MINHA CONTA: Cookie não encontrado. Redirecionando para /login.")
            return self.redirecionar('/login')

        # 2. Espião para ver todos os IDs que o UserModel conhece AGORA
        lista_ids_no_modelo = [u.id for u in self.user_model.get_all()]
        print(f"DEBUG MINHA CONTA: IDs de usuário que o modelo conhece: {lista_ids_no_modelo}")

        # 3. Tentativa de buscar o usuário
        usuario = self.user_model.get_by_id(id_usuario_logado)
        
        if not usuario:
            # 4. Espião para nos dizer se a busca falhou
            print(f"DEBUG MINHA CONTA: ERRO! Usuário com ID '{id_usuario_logado}' não encontrado na lista acima. Deslogando.")
            return self.redirecionar('/logout')

        # Se chegou até aqui, a busca foi um sucesso.
        print(f"DEBUG MINHA CONTA: Sucesso! Usuário '{usuario.name}' encontrado. Carregando página.")
        todas_as_reservas = self.reserva_model.get_all()
        reservas_do_usuario = [r for r in todas_as_reservas if r.user and r.user.id == id_usuario_logado]
        
        return self.renderizar('minha_conta', usuario=usuario, reservas=reservas_do_usuario, titulo="Minha Conta")