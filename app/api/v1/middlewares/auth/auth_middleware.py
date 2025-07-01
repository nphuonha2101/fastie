from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

from app.api.v1.middlewares.abstract_middleware import AbstractMiddleware


class AuthMiddleware(AbstractMiddleware):
    async def handle(self, request: Request, credentials: HTTPAuthorizationCredentials):

        pass