import sys
import os

diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(diretorio_raiz)

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
