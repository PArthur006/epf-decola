import pytest
from unittest.mock import MagicMock, patch
from controllers.controlador_pagamento import ControladorPagamento
from models import Voo, Destino, User
from datetime import datetime

@pytest.fixture
def mock_app():
    return MagicMock()

@pytest.fixture
def pagamento_controller(mock_app):
    return ControladorPagamento(mock_app)

# Teste para verificar se a página de pagamento é renderizada corretamente com os dados da reserva.
def test_pagina_pagamento(pagamento_controller, db_session):
    # Preenche o banco de dados com um destino, um voo e um usuário
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
    user = User(
        id='U001', name='Test User', email='test@example.com',
        password='hashed_password', birthdate='N/A', cpf='123.456.789-00', nationality='N/A'
    )
    db_session.add(voo)
    db_session.add(user)
    db_session.commit()

    with patch.object(pagamento_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_pagamento.get_db', return_value=iter([db_session])), \
         patch.object(pagamento_controller, 'obter_usuario_logado', return_value='U001'):

        pagamento_controller.pagina_pagamento("TC001", "A1,A2")

        mock_renderizar.assert_called_once()
        args, kwargs = mock_renderizar.call_args
        assert 'reserva' in kwargs
        assert kwargs['reserva'].voo.numero_voo == "TC001"
        assert kwargs['reserva'].assentos == ["A1", "A2"]
