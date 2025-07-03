import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

from app.api.v1.middlewares.abstract_middleware import AbstractMiddleware
from app.core.decorators.di import component


@component
class AuthMiddleware(AbstractMiddleware):
    def __init__(self):
        self.secret_key = "your-secret-key"  # Should be configured in environment variable
        self.algorithm = "HS256"

    async def handle(self, request: Request, credentials: HTTPAuthorizationCredentials):
        """
        Handle JWT token authentication
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không được cung cấp",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            # Decode JWT token
            payload = jwt.decode(
                credentials.credentials, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token không hợp lệ",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Save user_id to request state to use in controller
            request.state.user_id = user_id
            return {"user_id": user_id}
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token đã hết hạn",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ",
                headers={"WWW-Authenticate": "Bearer"},
            )