import pytest
from unittest.mock import MagicMock, patch
from controllers.controlador_autenticacao import ControladorAutenticacao
from models.user import User
from bottle import request, HTTPResponse
import bcrypt

@pytest.fixture
def mock_app():
    return MagicMock()

@pytest.fixture
def auth_controller(mock_app):
    # O controlador não recebe mais o modelo no construtor
    return ControladorAutenticacao(mock_app)

# Teste para verificar o cadastro de um novo usuário com sucesso.
def test_efetuar_cadastro_success(auth_controller, db_session):
    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'birthdate': '2000-01-01',
            'cpf': '123.456.789-00',
            'nationality': 'Brazilian'
        }.get(key)

        with pytest.raises(HTTPResponse) as e:
            auth_controller.efetuar_cadastro()
        
        assert e.value.status_code in [302, 303] # Redirecionar
        assert e.value.headers['Location'].endswith('/login')

        user = db_session.query(User).filter_by(email='test@example.com').first()
        assert user is not None
        assert user.name == 'Test User'
        assert user.cpf == '123.456.789-00'


# Teste para verificar o cenário onde as senhas não coincidem durante o cadastro.
def test_efetuar_cadastro_password_mismatch(auth_controller, db_session):
    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'mismatch',
            'birthdate': '2000-01-01',
            'cpf': '123.456.789-00',
            'nationality': 'Brazilian'
        }.get(key)

        response = auth_controller.efetuar_cadastro()

        user = db_session.query(User).filter_by(email='test@example.com').first()
        assert user is None
        assert "As senhas não coincidem." in response

# Teste para verificar o cenário onde o email já está em uso durante o cadastro.
def test_efetuar_cadastro_email_in_use(auth_controller, db_session):
    # Preenche o banco de dados com um usuário
    existing_user = User(
        id='U001', name='Existing User', email='existing@example.com',
        password='hashed_password', birthdate='N/A', cpf='111.111.111-11', nationality='N/A'
    )
    db_session.add(existing_user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'existing@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'birthdate': '2000-01-01',
            'cpf': '123.456.789-00',
            'nationality': 'Brazilian'
        }.get(key)

        response = auth_controller.efetuar_cadastro()
        assert "Este email já está em uso." in response

# Teste para verificar o cenário onde o CPF já está em uso durante o cadastro.
def test_efetuar_cadastro_cpf_in_use(auth_controller, db_session):
    # Preenche o banco de dados com um usuário
    existing_user = User(
        id='U001', name='Existing User', email='another@example.com',
        password='hashed_password', birthdate='N/A', cpf='123.456.789-00', nationality='N/A'
    )
    db_session.add(existing_user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'birthdate': '2000-01-01',
            'cpf': '123.456.789-00',
            'nationality': 'Brazilian'
        }.get(key)

        response = auth_controller.efetuar_cadastro()
        assert "Este CPF já está em uso." in response


# Teste para verificar o login de um usuário com credenciais válidas.
def test_efetuar_login_success(auth_controller, db_session):
    hashed_password = bcrypt.hashpw(b'password123', bcrypt.gensalt())
    user = User(
        id='U001', name='Test User', email='test@example.com',
        password=hashed_password.decode('utf-8'), birthdate='2000-01-01', cpf='123.456.789-00', nationality='Brazilian'
    )
    db_session.add(user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.response') as mock_response, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'email': 'test@example.com',
            'password': 'password123'
        }.get(key)

        with pytest.raises(HTTPResponse) as e:
            auth_controller.efetuar_login()
        
        assert e.value.status_code in [302, 303]
        assert e.value.headers['Location'].endswith('/voos')
        mock_response.set_cookie.assert_called_once()


# Teste para verificar o login de um usuário com credenciais inválidas.
def test_efetuar_login_invalid_credentials(auth_controller, db_session):
    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }.get(key)

        response = auth_controller.efetuar_login()
        assert "Email ou senha inválidos." in response
