from dotenv import load_dotenv
from fastapi import FastAPI
from app.core.providers.app_service_providers import initialize_application
from app.routes.api import register_routes

load_dotenv()
initialize_application()
app = FastAPI()

register_routes(app)