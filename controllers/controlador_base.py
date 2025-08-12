from bottle import static_file, template, redirect, request
from config import Config

class ControladorBase:
    """
    Classe base para todos os outros controllers.
    Fornece métodos úteis como renderizar, redirecionar e servir arquivos estáticos,
    além de verificar o status de login do usuário.
    """
    def __init__(self, app):
        """Construtor que armazena a instância da aplicação Bottle."""
        self.app = app
        self._configurar_rotas_base()

    def _configurar_rotas_base(self):
        """Configura rotas comuns a toda a aplicação."""
        # Rota para servir arquivos estáticos (CSS, JS, imagens, etc.).
        self.app.route('/static/<nome_arquivo:path>', callback=self.servir_arquivo_estatico)

    def servir_arquivo_estatico(self, nome_arquivo):
        """Busca e serve um arquivo da pasta /static."""
        return static_file(nome_arquivo, root='./static')

    def renderizar(self, nome_template, **contexto):
        """
        Método auxiliar para renderizar um template da pasta /views.
        Ele automaticamente verifica se o usuário está logado e passa essa
        informação para todos os templates.
        """
        # Lê o cookie 'user_id' para determinar o estado de login do usuário.
        id_usuario_logado = request.get_cookie("user_id", secret=Config.CHAVE_SECRETA)
        
        # Adiciona a variável 'usuario_logado' (True or False) ao contexto do template.
        contexto['usuario_logado'] = id_usuario_logado is not None
        
        # Renderiza o template com o contexto fornecido.
        return template(nome_template, **contexto)

    def redirecionar(self, caminho):
        """Método auxiliar para fazer redirecionamemntos de URL."""
        return redirect(caminho)

    def obter_usuario_logado(self):
        """Lê o cookie e retorna o ID do usuário logado, se existir."""
        return request.get_cookie("user_id", secret=Config.CHAVE_SECRETA)