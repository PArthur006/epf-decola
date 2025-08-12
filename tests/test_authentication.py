import pytest
from unittest.mock import MagicMock, patch
from controllers.controlador_autenticacao import ControladorAutenticacao
from models.user import UserModel, User
from config import Config
from bottle import request

# Mock the Config.CHAVE_SECRETA for testing purposes
@pytest.fixture(autouse=True)
def mock_config_secret_key():
    with patch('config.Config.CHAVE_SECRETA', 'test-secret-key'):
        yield

@pytest.fixture(autouse=True)
def mock_bottle_template():
    with patch('bottle.template') as mock_template:
        def _template_side_effect(name, **context):
            if 'erro' in context and context['erro']:
                return f"Template {name} rendered with error: {context['erro']}"
            return f"Template {name} rendered successfully."
        mock_template.side_effect = _template_side_effect
        yield mock_template

@pytest.fixture(autouse=True)
def mock_base_controller_render():
    with patch('controllers.controlador_base.ControladorBase.renderizar') as mock_renderizar:
        def _renderizar_side_effect(name, **context):
            if 'erro' in context and context['erro']:
                return f"Template {name} rendered with error: {context['erro']}"
            return f"Template {name} rendered successfully."
        mock_renderizar.side_effect = _renderizar_side_effect
        yield mock_renderizar

@pytest.fixture
def mock_app():
    return MagicMock()

@pytest.fixture
def mock_user_model():
    return MagicMock(spec=UserModel)

@pytest.fixture
def auth_controller(mock_app, mock_user_model):
    return ControladorAutenticacao(mock_app, mock_user_model)

def test_efetuar_cadastro_success(auth_controller, mock_user_model):
    # Mock request.forms
    with patch.object(request.forms, 'get') as mock_forms_get, \
         patch.object(auth_controller, 'redirecionar') as mock_redirecionar:
        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)

        mock_user_model.get_by_email.return_value = None
        mock_user_model.gerar_proximo_id.return_value = 'U001'

        response = auth_controller.efetuar_cadastro()
        
        mock_user_model.add_user.assert_called_once()
        mock_redirecionar.assert_called_once_with('/login')

def test_efetuar_cadastro_password_mismatch(auth_controller, mock_user_model):
    with patch.object(request.forms, 'get') as mock_forms_get:
        mock_forms_get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'mismatch'
        }.get(key)

        mock_user_model.get_by_email.return_value = None # Ensure email is not found

        response = auth_controller.efetuar_cadastro()
        
        mock_user_model.add_user.assert_not_called()
        assert "Template cadastro rendered with error: As senhas não coincidem." == response

def test_efetuar_cadastro_email_in_use(auth_controller, mock_user_model):
    with patch('bottle.request') as mock_request:
        mock_request.forms = MagicMock()
        mock_request.forms.get.side_effect = lambda key: {
            'nome': 'Test User',
            'email': 'existing@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)

        mock_user_model.get_by_email.return_value = User(
            user_id='U001', name='Existing User', email='existing@example.com',
            password='hashed_password', birthdate='N/A', cpf='N/A', nationality='N/A'
        )

        response = auth_controller.efetuar_cadastro()
        
        mock_user_model.add_user.assert_not_called()
        assert "Template cadastro rendered with error: Este email já está em uso." == response

def test_efetuar_login_success(auth_controller, mock_user_model):
    with patch.object(request.forms, 'get') as mock_forms_get, \
         patch('controllers.controlador_autenticacao.response') as mock_auth_response, \
         patch('bcrypt.checkpw', return_value=True), \
         patch.object(auth_controller, 'redirecionar') as mock_redirecionar:
        
        mock_forms_get.side_effect = lambda key: {
            'email': 'test@example.com',
            'password': 'password123'
        }.get(key)

        mock_user_model.get_by_email.return_value = User(
            user_id='U001', name='Test User', email='test@example.com',
            password=b'hashed_password', # Make it a byte string
            birthdate='N/A', cpf='N/A', nationality='N/A'
        )

        response = auth_controller.efetuar_login()
        
        mock_auth_response.set_cookie.assert_called_once_with(
            "user_id", "U001", secret="test-secret-key", path="/"
        )
        mock_redirecionar.assert_called_once_with('/voos')

def test_efetuar_login_invalid_credentials(auth_controller, mock_user_model):
    with patch('bottle.request') as mock_request, \
         patch('bcrypt.checkpw', return_value=False):
        
        mock_request.forms = MagicMock()
        mock_request.forms.get.side_effect = lambda key: {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }.get(key)

        mock_user_model.get_by_email.return_value = None # User not found or password mismatch

        response = auth_controller.efetuar_login()
        
        assert "Template login rendered with error: Email ou senha inválidos." == response