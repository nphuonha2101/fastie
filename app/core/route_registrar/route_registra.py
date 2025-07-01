from fastapi import APIRouter, FastAPI, Depends
from typing import List, Type, Callable

from app.core.service_containers.service_containers import get_registry


class RouteRegistrar:
    """
    A class to register API routes in a FastAPI application.
    This class allows for modular route registration by encapsulating the logic
    for registering controllers and their routes under a specified prefix.
    """
    def __init__(self, app: FastAPI, prefix: str = "/api/v1"):
        self.app = app
        self.api_router = APIRouter(prefix=prefix)
        self.registry = get_registry()

    def register(
            self,
            controller_class: Type,
            prefix: str = "",
            tags: List[str] = None,
            middleware: List[Callable] = None
    ):
        controller = self.registry.resolve(controller_class)
        if not controller or not hasattr(controller, 'router'):
            raise ValueError(f"Controller {controller_class.__name__} is not properly registered or does not have a router.")

        sub_router = APIRouter(
            prefix=prefix,
            tags=tags or [],
            dependencies=[Depends(m) for m in (middleware or [])]
        )

        sub_router.include_router(controller.router)

        self.api_router.include_router(sub_router)

    def apply(self):
        self.app.include_router(self.api_router)