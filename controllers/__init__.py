from bottle import Bottle
from controllers.user_controller import user_routes
from .user_controller import UserController
from .auth_controller import AuthController
from .flight_controller import FlightController


def init_controllers(app: Bottle):
    app.merge(user_routes)
    user_controller = UserController(app)

    auth_controller = AuthController(app)

    flight_controller = FlightController(app)
