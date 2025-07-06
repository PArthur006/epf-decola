# controllers/controlador_base.py (VERSÃO FINAL)

from bottle import static_file, template, redirect, request

class ControladorBase:
    """
    Classe base para todos os outros controllers.
    Fornece métodos úteis como renderizar, redirecionar e servir arquivos estáticos.
    """
    def __init__(self, app):
        self.app = app
        self._configurar_rotas_base()

    def _configurar_rotas_base(self):
        """Configura rotas comuns, como a de arquivos estáticos."""
        self.app.route('/static/<nome_arquivo:path>', callback=self.servir_arquivo_estatico)

    def servir_arquivo_estatico(self, nome_arquivo):
        """Serve arquivos da pasta /static."""
        return static_file(nome_arquivo, root='./static')

    def renderizar(self, nome_template, **contexto):
        """
        Método auxiliar que verifica o status de login e o passa para todos os templates.
        """
        # Verifica se o usuário está logado através do cookie
        id_usuario_logado = request.get_cookie("user_id", secret='sua-chave-secreta-aqui')
        contexto['usuario_logado'] = id_usuario_logado is not None
        
        return template(nome_template, **contexto)

    def redirecionar(self, caminho):
        """Método auxiliar para redirecionamentos."""
        return redirect(caminho)

    def obter_usuario_logado(self):
        """Verifica o cookie e retorna o ID do usuário logado, se houver."""
        return request.get_cookie("user_id", secret='sua-chave-secreta-aqui')