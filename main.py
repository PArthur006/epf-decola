import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH para que os módulos possam ser importados.
diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(diretorio_raiz)

from app import create_app

# Ponto de entrada principal da aplicação.
if __name__ == '__main__':
    app = create_app()
    app.run()
