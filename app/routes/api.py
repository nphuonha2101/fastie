from fastapi import FastAPI

from app.api.v1.controllers.auth.auth_controller import AuthController
from app.api.v1.controllers.user_account.user_account_controller import UserAccountController
from app.core.route_registrar.route_registra import RouteRegistrar

def register_routes(app: FastAPI):
    route_registrar = RouteRegistrar(app)

    # Register the AuthController routes
    route_registrar.register(AuthController, "/auth", ["Auth"])
    route_registrar.register(UserAccountController, "/user", ["UserAccount"])

    route_registrar.apply()
