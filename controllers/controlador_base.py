from bottle import static_file, template as render_template, redirect as bottle_redirect

class ControladorBase:
    """
    Classe base para todos os outros controllers.
    Fornece métodos úteis e configura rotas comuns.
    """
    def __init__(self, app):
        # Armazena a instância principal da aplicação Bottle
        self.app = app
        # Chama o método para configurar as rotas base
        self._configurar_rotas_base()

    def _configurar_rotas_base(self):
        """Configura rotas básicas, como a rota para arquivos estáticos."""
        # Rota para servir arquivos estáticos (CSS, JS, imagens)
        self.app.route('/static/<nome_arquivo:path>', callback=self.servir_arquivo_estatico)

    def redirecionar_home(self):
        """Redireciona a rota raiz para a página inicial de voos."""
        return self.redirecionar('/voos')

    def servir_arquivo_estatico(self, nome_arquivo):
        """Serve arquivos da pasta /static."""
        return static_file(nome_arquivo, root='./static')

    def renderizar(self, nome_template, **contexto):
        """Método auxiliar para renderizar templates da pasta /views."""
        return render_template(nome_template, **contexto)

    def redirecionar(self, caminho):
        """Método auxiliar para redirecionamentos."""
        return bottle_redirect(caminho)