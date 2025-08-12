import pytest
from unittest.mock import MagicMock, patch
from controllers.controlador_voo import ControladorVoo
from models import Voo, Destino
from datetime import datetime

@pytest.fixture
def mock_app():
    return MagicMock()

@pytest.fixture
def voo_controller(mock_app):
    return ControladorVoo(mock_app)

# Teste para verificar se a listagem de voos funciona corretamente.
def test_listar_voos(voo_controller, db_session):
    # Preenche o banco de dados com um destino e um voo
    destino = Destino(cidade="Test City", pais="Test Country", aeroporto="TCY", imagem="img.png")
    db_session.add(destino)
    db_session.commit()

    voo = Voo(
        numero_voo="TC001",
        preco=100.0,
        data_partida=datetime(2025, 12, 24, 10, 0, 0),
        data_chegada=datetime(2025, 12, 24, 12, 0, 0),
        assentos_total=100,
        comp_aerea="Test Air",
        destino_id=destino.id
    )
    db_session.add(voo)
    db_session.commit()

    with patch.object(voo_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_voo.get_db', return_value=iter([db_session])):

        voo_controller.listar_voos()

        mock_renderizar.assert_called_once()
        args, kwargs = mock_renderizar.call_args
        assert 'voos' in kwargs
        assert len(kwargs['voos']) == 1
        assert kwargs['voos'][0].numero_voo == "TC001"

