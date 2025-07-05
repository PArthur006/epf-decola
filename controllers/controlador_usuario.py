from bottle import request
from .controlador_base import ControladorBase

# A linha "from services.servico_usuario import ServicoUsuario" foi REMOVIDA por enquanto.

class ControladorUsuario(ControladorBase):
    """
    Controller para gerenciar as rotas relacionadas aos usuários (CRUD).
    ATENÇÃO: Este controller está temporariamente desacoplado da camada de serviço.
    """
    def __init__(self, app):
        super().__init__(app)
        # A linha "self.servico_usuario = ServicoUsuario()" foi REMOVIDA por enquanto.
        self.configurar_rotas()

    def configurar_rotas(self):
        """Define as rotas de CRUD de usuário."""
        self.app.route('/usuarios', method='GET', callback=self.listar_usuarios)
        self.app.route('/usuarios/adicionar', method=['GET', 'POST'], callback=self.adicionar_usuario)
        self.app.route('/usuarios/editar/<id_usuario>', method=['GET', 'POST'], callback=self.editar_usuario)
        self.app.route('/usuarios/deletar/<id_usuario>', method='POST', callback=self.deletar_usuario)

    def listar_usuarios(self):
        """Busca todos os usuários e renderiza a página de listagem."""
        # TODO: A linha abaixo será descomentada quando o ServicoUsuario estiver pronto.
        # usuarios = self.servico_usuario.obter_todos()
        
        # Por enquanto, usamos uma lista vazia para não dar erro no template.
        usuarios_exemplo = []
        
        # Renderiza o template 'usuarios.tpl' (que precisaria ser criado)
        return self.renderizar('usuarios', usuarios=usuarios_exemplo, titulo="Lista de Usuários")

    def adicionar_usuario(self):
        """Lida com a adição de um novo usuário."""
        if request.method == 'GET':
            # Mostra o formulário de adição.
            return self.renderizar('formulario_usuario', usuario=None, acao="/usuarios/adicionar")
        else: # POST
            # TODO: Aqui entrará a chamada para o serviço para salvar o novo usuário.
            # Ex: dados_formulario = request.forms
            #     self.servico_usuario.criar_usuario(dados_formulario)
            print("Formulário de adição recebido. Redirecionando...")
            self.redirecionar('/usuarios')

    def editar_usuario(self, id_usuario):
        """Lida com a edição de um usuário existente."""
        # TODO: Aqui entrará a chamada para o serviço para buscar o usuário pelo ID.
        # usuario = self.servico_usuario.obter_por_id(id_usuario)
        
        # Por enquanto, usamos um dicionário vazio como dado de exemplo.
        usuario_exemplo = {'id': id_usuario, 'name': 'Usuário de Teste', 'email': 'teste@email.com'}
        
        if not usuario_exemplo: # A verificação continuará funcionando
            return "Usuário não encontrado"

        if request.method == 'GET':
            # Mostra o formulário preenchido com os dados do usuário.
            return self.renderizar('formulario_usuario', usuario=usuario_exemplo, acao=f"/usuarios/editar/{id_usuario}")
        else: # POST
            # TODO: Aqui entrará a chamada para o serviço para salvar as alterações.
            # Ex: dados_formulario = request.forms
            #     self.servico_usuario.atualizar_usuario(id_usuario, dados_formulario)
            print(f"Formulário de edição para o usuário {id_usuario} recebido. Redirecionando...")
            self.redirecionar('/usuarios')

    def deletar_usuario(self, id_usuario):
        """Processa a requisição para deletar um usuário."""
        # TODO: Aqui entrará a chamada para o serviço para deletar o usuário.
        # self.servico_usuario.deletar_usuario(id_usuario)
        print(f"Requisição para deletar o usuário {id_usuario} recebida. Redirecionando...")
        self.redirecionar('/usuarios')