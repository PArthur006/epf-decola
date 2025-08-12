import pytest
from unittest.mock import MagicMock, patch
from controllers.controlador_autenticacao import ControladorAutenticacao
from models.user import User
from bottle import request
import bcrypt

@pytest.fixture
def mock_app():
    return MagicMock()

@pytest.fixture
def auth_controller(mock_app):
    # The controller no longer takes the model in the constructor
    return ControladorAutenticacao(mock_app)

def test_efetuar_cadastro_success(auth_controller, db_session):
    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch.object(auth_controller, 'redirecionar') as mock_redirecionar, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)

        auth_controller.efetuar_cadastro()

        user = db_session.query(User).filter_by(email='test@example.com').first()
        assert user is not None
        assert user.name == 'Test User'
        mock_redirecionar.assert_called_once_with('/login')

def test_efetuar_cadastro_password_mismatch(auth_controller, db_session):
    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch.object(auth_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'mismatch'
        }.get(key)

        auth_controller.efetuar_cadastro()

        user = db_session.query(User).filter_by(email='test@example.com').first()
        assert user is None
        mock_renderizar.assert_called_once_with('cadastro', erro='As senhas não coincidem.')

def test_efetuar_cadastro_email_in_use(auth_controller, db_session):
    # Pre-populate the database with a user
    existing_user = User(
        id='U001', name='Existing User', email='existing@example.com',
        password='hashed_password', birthdate='N/A', cpf='123.456.789-00', nationality='N/A'
    )
    db_session.add(existing_user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch.object(auth_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'existing@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)

        auth_controller.efetuar_cadastro()
        mock_renderizar.assert_called_once_with('cadastro', erro='Este email já está em uso.')

def test_efetuar_login_success(auth_controller, db_session):
    hashed_password = bcrypt.hashpw(b'password123', bcrypt.gensalt())
    user = User(
        id='U001', name='Test User', email='test@example.com',
        password=hashed_password.decode('utf-8'), birthdate='N/A', cpf='123.456.789-00', nationality='N/A'
    )
    db_session.add(user)
    db_session.commit()

    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.response') as mock_response, \
         patch.object(auth_controller, 'redirecionar') as mock_redirecionar, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'email': 'test@example.com',
            'password': 'password123'
        }.get(key)

        auth_controller.efetuar_login()

        mock_response.set_cookie.assert_called_once()
        mock_redirecionar.assert_called_once_with('/voos')

def test_efetuar_login_invalid_credentials(auth_controller, db_session):
    with patch('bottle.request.forms.get') as mock_forms_get, \
         patch.object(auth_controller, 'renderizar') as mock_renderizar, \
         patch('controllers.controlador_autenticacao.get_db', return_value=iter([db_session])):

        mock_forms_get.side_effect = lambda key: {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }.get(key)

        auth_controller.efetuar_login()
        mock_renderizar.assert_called_once_with('login', erro='Email ou senha inválidos.')