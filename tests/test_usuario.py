import pytest
from unittest.mock import MagicMock, patch
from controllers.controlador_usuario import ControladorUsuario
from models import User, Reserva, Voo, Destino
from datetime import datetime
from bottle import request, HTTPResponse
import bcrypt
import uuid

@pytest.fixture
def mock_app():
    return MagicMock()

@pytest.fixture
def usuario_controller(mock_app):
    return ControladorUsuario(mock_app)

# Teste para verificar a validação de CPFs válidos.
def test_validar_cpf_validos():
    assert User.validar_cpf("123.456.789-09") == True
    assert User.validar_cpf("987.654.321-00") == True

# Teste para verificar a validação de CPFs inválidos.
def test_validar_cpf_invalidos():
    assert User.validar_cpf("000.000.000-00") == False # Todos os zeros
    assert User.validar_cpf("111.111.111-11") == False # Todos os uns
    assert User.validar_cpf("222.222.222-22") == False # Todos os dois
    assert User.validar_cpf("333.333.333-33") == False # Todos os três
    assert User.validar_cpf("444.444.444-44") == False # Todos os quatros
    assert User.validar_cpf("555.555.555-55") == False # Todos os cincos
    assert User.validar_cpf("666.666.666-66") == False # Todos os seis
    assert User.validar_cpf("777.777.777-77") == False # Todos os setes
    assert User.validar_cpf("888.888.888-88") == False # Todos os oitos
    assert User.validar_cpf("999.999.999-99") == False # Todos os noves
    assert User.validar_cpf("123") == False # Muito curto
    assert User.validar_cpf("123.456.789-0") == False # Muito curto
    assert User.validar_cpf("123456789012") == False # Muito longo
    assert User.validar_cpf("abc.def.ghi-jk") == False # Não-dígitos
    assert User.validar_cpf("111.111.111-12") == False # Último dígito inválido
    assert User.validar_cpf("123.456.789-10") == False # Último dígito inválido

# Teste para verificar se a página "Minha Conta" é renderizada corretamente com os dados do usuário e suas reservas.
def test_pagina_minha_conta(usuario_controller, db_session):
    # Pre-populate the database with a user and a reservation
    user = User(
        id='U001', name='Test User', email='test@example.com',
        password='hashed_password', birthdate='01/01/1990', cpf='123.456.789-00', nationality='Brazilian', phone='11987654321'
    )
    destino = Destino(cidade="Test City", pais="Test Country", aeroporto="TCY", imagem="img.png")
    db_session.add(user)
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

    reserva = Reserva(
        user_id='U001',
        voo_id='TC001',
        assento='A1',
        status='Confirmada'
    )
    db_session.add(reserva)
    db_session.commit()

    with patch.object(usuario_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_usuario.get_db', return_value=iter([db_session])), \
         patch.object(usuario_controller, 'obter_usuario_logado', return_value='U001'):

        usuario_controller.pagina_minha_conta()

        mock_renderizar.assert_called_once()
        args, kwargs = mock_renderizar.call_args
        assert 'usuario' in kwargs
        assert 'reservas' in kwargs
        assert kwargs['usuario'].name == 'Test User'
        assert len(kwargs['reservas']) == 1
        assert kwargs['reservas'][0].assento == 'A1'

# Teste para verificar a edição bem-sucedida dos dados da conta do usuário.
def test_editar_minha_conta_success(usuario_controller, db_session):
    hashed_password = bcrypt.hashpw(b'old_password', bcrypt.gensalt())
    user = User(
        id='U001', name='Old Name', email='old@example.com',
        password=hashed_password.decode('utf-8'), birthdate='01/01/1990', cpf='123.456.789-00', nationality='Brazilian', phone='11987654321'
    )
    db_session.add(user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_usuario.get_db', return_value=iter([db_session])), \
         patch.object(usuario_controller, 'obter_usuario_logado', return_value='U001'):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'New Name',
            'email': 'new@example.com',
            'password': '',
            'confirm_password': '',
            'birthdate': '01/01/1990',
            'cpf': '123.456.789-09',
            'nationality': 'Brazilian',
            'phone': '11987654321'
        }.get(key)

        with pytest.raises(HTTPResponse) as e:
            usuario_controller.editar_minha_conta()
        
        assert e.value.status_code in [302, 303]
        assert e.value.headers['Location'].endswith('/minha-conta')

        updated_user = db_session.query(User).filter_by(id='U001').first()
        assert updated_user.name == 'New Name'
        assert updated_user.email == 'new@example.com'
        assert bcrypt.checkpw(b'old_password', updated_user.password.encode('utf-8'))

# Teste para verificar a alteração de senha na edição da conta do usuário.
def test_editar_minha_conta_password_change(usuario_controller, db_session):
    hashed_password = bcrypt.hashpw(b'old_password', bcrypt.gensalt())
    user = User(
        id='U001', name='Old Name', email='old@example.com',
        password=hashed_password.decode('utf-8'), birthdate='01/01/1990', cpf='123.456.789-00', nationality='Brazilian', phone='11987654321'
    )
    db_session.add(user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_usuario.get_db', return_value=iter([db_session])), \
         patch.object(usuario_controller, 'obter_usuario_logado', return_value='U001'):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Old Name',
            'email': 'old@example.com',
            'password': 'new_password',
            'confirm_password': 'new_password',
            'birthdate': '01/01/1990',
            'cpf': '123.456.789-09',
            'nationality': 'Brazilian',
            'phone': '11987654321'
        }.get(key)

        with pytest.raises(HTTPResponse) as e:
            usuario_controller.editar_minha_conta()
        
        assert e.value.status_code in [302, 303]
        assert e.value.headers['Location'].endswith('/minha-conta')

        updated_user = db_session.query(User).filter_by(id='U001').first()
        assert bcrypt.checkpw(b'new_password', updated_user.password.encode('utf-8'))

# Teste para verificar o cenário onde as senhas não coincidem durante a edição da conta.
def test_editar_minha_conta_password_mismatch(usuario_controller, db_session):
    hashed_password = bcrypt.hashpw(b'old_password', bcrypt.gensalt())
    user = User(
        id='U001', name='Old Name', email='old@example.com',
        password=hashed_password.decode('utf-8'), birthdate='01/01/1990', cpf='123.456.789-00', nationality='Brazilian', phone='11987654321'
    )
    db_session.add(user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch.object(usuario_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_usuario.get_db', return_value=iter([db_session])), \
         patch.object(usuario_controller, 'obter_usuario_logado', return_value='U001'):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Old Name',
            'email': 'old@example.com',
            'password': 'new_password',
            'confirm_password': 'mismatch',
            'birthdate': '01/01/1990',
            'cpf': '123.456.789-09',
            'nationality': 'Brazilian',
            'phone': '11987654321'
        }.get(key)

        usuario_controller.editar_minha_conta()
        assert "As senhas não coincidem." in mock_renderizar.call_args[1]['erro']

# Teste para verificar o cenário onde o email já está em uso por outro usuário durante a edição da conta.
def test_editar_minha_conta_email_in_use(usuario_controller, db_session):
    hashed_password = bcrypt.hashpw(b'old_password', bcrypt.gensalt())
    user = User(
        id='U001', name='Old Name', email='old@example.com',
        password=hashed_password.decode('utf-8'), birthdate='01/01/1990', cpf='123.456.789-00', nationality='Brazilian', phone='11987654321'
    )
    another_user = User(
        id='U002', name='Another User', email='another@example.com',
        password=hashed_password.decode('utf-8'), birthdate='01/01/1990', cpf='987.654.321-00', nationality='Brazilian', phone='11987654321'
    )
    db_session.add(user)
    db_session.add(another_user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch.object(usuario_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_usuario.get_db', return_value=iter([db_session])), \
         patch.object(usuario_controller, 'obter_usuario_logado', return_value='U001'):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Old Name',
            'email': 'another@example.com',
            'password': '',
            'confirm_password': '',
            'birthdate': '01/01/1990',
            'cpf': '123.456.789-09',
            'nationality': 'Brazilian',
            'phone': '11987654321'
        }.get(key)

        usuario_controller.editar_minha_conta()
        assert "Este email já está em uso por outro usuário." in mock_renderizar.call_args[1]['erro']