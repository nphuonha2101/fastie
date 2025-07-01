from app.core.decorators.di import repository
from app.core.service_containers.service_containers import get_registry
from app.repositories.interfaces.user.i_user_repository import IUserRepository
from app.repositories.implements.repository import Repository, TCreate, T
from app.models.user import User

registry = get_registry()

@repository
class UserRepository(Repository, IUserRepository):
    def __init__(self):
        super().__init__(User)


