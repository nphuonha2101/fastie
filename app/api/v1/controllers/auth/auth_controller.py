from abc import ABC

from app.api.v1.controllers.base_controller import BaseController
from app.core.decorators.di import controller, inject

@controller
class AuthController(BaseController, ABC):

    def __init__(self):
        super().__init__()

    def define_routes(self):
        self.router.post("/login", summary="User Login", status_code=200)(self.login)
        self.router.get("/greet", summary="Greeting Endpoint", status_code=200)(self.greet)


    def login(self):
        """
        Handles user login.
        :return: Success message with user data.
        """
        # Implement login logic here
        return self.success(content={"message": "Login successful"})

    def greet(self):
        """
        Handles greeting.
        :return: Greeting message.
        """
        return self.error(message="Hello, welcome to the API!", status_code=400)




