#!/usr/bin/env python3
"""
Fastie CLI - A command line interface for Fastie framework
Similar to Laravel Artisan
"""

import click
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import shutil


@click.group()
@click.version_option(version='1.0.0', prog_name='Fastie CLI')
def cli():
    """Fastie Framework CLI - Laravel Artisan-like command line interface"""
    pass


# =============================================================================
# PROJECT COMMANDS
# =============================================================================

@cli.command()
@click.argument('project_name')
@click.option('--database', '-d', default='mysql', help='Database type (mysql, sqlite, postgres)')
@click.option('--auth', is_flag=True, help='Include authentication boilerplate')
def new(project_name, database, auth):
    """Create a new Fastie project"""
    click.echo(f"🚀 Creating new Fastie project: {project_name}")
    
    try:
        # Create project directory
        project_path = Path(project_name)
        if project_path.exists():
            click.echo(f"❌ Directory {project_name} already exists!")
            return
        
        # Copy current project structure as template
        current_dir = Path.cwd()
        shutil.copytree(current_dir, project_path, ignore=shutil.ignore_patterns(
            '__pycache__', '*.pyc', '.git', '.env', 'venv', 'node_modules', '.vscode'
        ))
        
        # Create .env file
        env_content = _generate_env_content(database)
        with open(project_path / '.env', 'w') as f:
            f.write(env_content)
        
        # Update README with project name
        readme_path = project_path / 'README.md'
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('Fastie', project_name.title())
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        click.echo(f"✅ Project {project_name} created successfully!")
        click.echo(f"📁 Next steps:")
        click.echo(f"   cd {project_name}")
        click.echo(f"   python -m venv venv")
        click.echo(f"   # Activate venv and install dependencies")
        click.echo(f"   pip install -r requirements.txt")
        click.echo(f"   python fastie.py db:migrate")
        click.echo(f"   python fastie.py serve")
        
    except Exception as e:
        click.echo(f"❌ Error creating project: {str(e)}")


# =============================================================================
# DATABASE COMMANDS
# =============================================================================

@cli.group(name='db')
def database():
    """Database related commands"""
    pass


@database.command(name='migrate')
def db_migrate():
    """Run database migrations"""
    click.echo("🔄 Running database migrations...")
    try:
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        click.echo("✅ Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Migration failed: {str(e)}")


@database.command(name='rollback')
@click.option('--steps', '-s', default=1, help='Number of steps to rollback')
def db_rollback(steps):
    """Rollback database migrations"""
    click.echo(f"⏪ Rolling back {steps} migration(s)...")
    try:
        for _ in range(steps):
            subprocess.run(['alembic', 'downgrade', '-1'], check=True)
        click.echo("✅ Rollback completed successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Rollback failed: {str(e)}")


@database.command(name='reset')
@click.confirmation_option(prompt='Are you sure you want to reset the database?')
def db_reset():
    """Reset database (rollback all migrations)"""
    click.echo("🔄 Resetting database...")
    try:
        subprocess.run(['alembic', 'downgrade', 'base'], check=True)
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        click.echo("✅ Database reset completed!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Database reset failed: {str(e)}")


@database.command(name='status')
def db_status():
    """Show migration status"""
    try:
        subprocess.run(['alembic', 'current'], check=True)
        subprocess.run(['alembic', 'history'], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to get database status: {str(e)}")


# =============================================================================
# MAKE COMMANDS
# =============================================================================

@cli.group(name='make')
def make():
    """Generate code files"""
    pass


@make.command(name='migration')
@click.argument('name')
@click.option('--table', '-t', help='Table name for migration')
def make_migration(name, table):
    """Create a new migration file"""
    click.echo(f"📝 Creating migration: {name}")
    try:
        if table:
            message = f"create_{table}_table"
        else:
            message = name.lower().replace(' ', '_')
        
        subprocess.run([
            'alembic', 'revision', '--autogenerate', '-m', message
        ], check=True)
        click.echo("✅ Migration created successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to create migration: {str(e)}")


@make.command(name='controller')
@click.argument('name')
@click.option('--resource', '-r', is_flag=True, help='Create resource controller with CRUD methods')
def make_controller(name, resource):
    """Create a new controller"""
    controller_name = f"{name.title()}Controller"
    path = Path(f"app/api/v1/controllers/{name.lower()}")
    path.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    (path / '__init__.py').touch()
    
    # Create controller file
    controller_content = _generate_controller_template(name, resource)
    controller_file = path / f"{name.lower()}_controller.py"
    
    with open(controller_file, 'w') as f:
        f.write(controller_content)
    
    click.echo(f"✅ Controller created: {controller_file}")
    
    # Update routes if needed
    _update_routes_registration(name)


@make.command(name='service')
@click.argument('name')
def make_service(name):
    """Create a new service"""
    # Create interface
    interface_path = Path(f"app/services/interfaces/{name.lower()}")
    interface_path.mkdir(parents=True, exist_ok=True)
    (interface_path / '__init__.py').touch()
    
    interface_content = _generate_service_interface_template(name)
    interface_file = interface_path / f"i_{name.lower()}_service.py"
    
    with open(interface_file, 'w') as f:
        f.write(interface_content)
    
    # Create implementation
    impl_path = Path(f"app/services/implements/{name.lower()}")
    impl_path.mkdir(parents=True, exist_ok=True)
    (impl_path / '__init__.py').touch()
    
    impl_content = _generate_service_implementation_template(name)
    impl_file = impl_path / f"{name.lower()}_service.py"
    
    with open(impl_file, 'w') as f:
        f.write(impl_content)
    
    click.echo(f"✅ Service created:")
    click.echo(f"   Interface: {interface_file}")
    click.echo(f"   Implementation: {impl_file}")


@make.command(name='repository')
@click.argument('name')
def make_repository(name):
    """Create a new repository"""
    # Create interface
    interface_path = Path(f"app/repositories/interfaces/{name.lower()}")
    interface_path.mkdir(parents=True, exist_ok=True)
    (interface_path / '__init__.py').touch()
    
    interface_content = _generate_repository_interface_template(name)
    interface_file = interface_path / f"i_{name.lower()}_repository.py"
    
    with open(interface_file, 'w') as f:
        f.write(interface_content)
    
    # Create implementation
    impl_path = Path(f"app/repositories/implements/{name.lower()}")
    impl_path.mkdir(parents=True, exist_ok=True)
    (impl_path / '__init__.py').touch()
    
    impl_content = _generate_repository_implementation_template(name)
    impl_file = impl_path / f"{name.lower()}_repository.py"
    
    with open(impl_file, 'w') as f:
        f.write(impl_content)
    
    click.echo(f"✅ Repository created:")
    click.echo(f"   Interface: {interface_file}")
    click.echo(f"   Implementation: {impl_file}")


@make.command(name='model')
@click.argument('name')
@click.option('--fields', '-f', help='Model fields (name:type,email:str)')
def make_model(name, fields):
    """Create a new model"""
    model_content = _generate_model_template(name, fields)
    model_file = Path(f"app/models/{name.lower()}.py")
    
    with open(model_file, 'w') as f:
        f.write(model_content)
    
    click.echo(f"✅ Model created: {model_file}")
    click.echo(f"💡 Don't forget to create migration: python fastie.py make:migration create_{name.lower()}_table")


@make.command(name='schema')
@click.argument('name')
@click.option('--type', 'schema_type', type=click.Choice(['request', 'response', 'model']), default='model')
def make_schema(name, schema_type):
    """Create a new schema"""
    if schema_type == 'request':
        path = Path(f"app/schemas/requests/{name.lower()}")
        file_name = f"{name.lower()}_request_schema.py"
    elif schema_type == 'response':
        path = Path(f"app/schemas/responses/{name.lower()}")
        file_name = f"{name.lower()}_response_schema.py"
    else:
        path = Path(f"app/schemas/models/{name.lower()}")
        file_name = f"{name.lower()}_base_schema.py"
    
    path.mkdir(parents=True, exist_ok=True)
    (path / '__init__.py').touch()
    
    schema_content = _generate_schema_template(name, schema_type)
    schema_file = path / file_name
    
    with open(schema_file, 'w') as f:
        f.write(schema_content)
    
    click.echo(f"✅ Schema created: {schema_file}")


# =============================================================================
# SERVER COMMANDS
# =============================================================================

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind')
@click.option('--port', default=8000, help='Port to bind')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(host, port, reload):
    """Start the development server"""
    click.echo(f"🚀 Starting Fastie server at http://{host}:{port}")
    
    cmd = ['uvicorn', 'app.main:app', '--host', host, '--port', str(port)]
    if reload:
        cmd.append('--reload')
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        click.echo("\n👋 Server stopped")


# =============================================================================
# UTILITY COMMANDS  
# =============================================================================

@cli.command()
def routes():
    """Show all registered routes"""
    click.echo("📋 Application Routes:")
    # This would need to be implemented to inspect the FastAPI app
    # For now, just show a placeholder
    click.echo("   GET  /docs          - API Documentation")
    click.echo("   GET  /redoc         - ReDoc Documentation")
    click.echo("   POST /auth/login    - User Login")
    click.echo("   GET  /auth/greet    - Greeting Endpoint")
    click.echo("   GET  /user/         - Get All Users")
    click.echo("   POST /user/register - Register User")


@cli.command()
def install():
    """Install project dependencies"""
    click.echo("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        click.echo("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to install dependencies: {str(e)}")


# =============================================================================
# TEMPLATE GENERATORS
# =============================================================================

def _generate_env_content(database):
    """Generate .env file content"""
    if database == 'sqlite':
        db_url = "sqlite:///./app.db"
    elif database == 'postgres':
        db_url = "postgresql+psycopg2://user:password@localhost:5432/dbname"
    else:  # mysql
        db_url = "mysql+pymysql://user:password@localhost:3306/dbname"
    
    return f"""# Database Configuration
DATABASE_URL={db_url}

# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# JWT Settings (if using authentication)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""


def _generate_controller_template(name, resource):
    """Generate controller template"""
    class_name = f"{name.title()}Controller"
    service_interface = f"I{name.title()}Service"
    
    template = f'''from abc import ABC
from app.api.v1.controllers.base_controller import BaseController
from app.core.decorators.di import controller, inject
from app.services.interfaces.{name.lower()}.i_{name.lower()}_service import {service_interface}

@controller
@inject
class {class_name}(BaseController, ABC):
    def __init__(self, {name.lower()}_service: {service_interface}):
        super().__init__()
        self.{name.lower()}_service = {name.lower()}_service

    def define_routes(self):
        """Define all routes for this controller"""'''
    
    if resource:
        template += f'''
        self.router.get("/", summary="Get All {name.title()}", status_code=200)(self.index)
        self.router.post("/", summary="Create {name.title()}", status_code=201)(self.create)
        self.router.get("/{{id}}", summary="Get {name.title()}", status_code=200)(self.show)
        self.router.put("/{{id}}", summary="Update {name.title()}", status_code=200)(self.update)
        self.router.delete("/{{id}}", summary="Delete {name.title()}", status_code=204)(self.delete)

    def index(self):
        """Get all {name.lower()}s"""
        try:
            {name.lower()}s = self.{name.lower()}_service.get_all()
            return self.success(content={name.lower()}s, message="{name.title()}s retrieved successfully.")
        except Exception as e:
            return self.error(message=str(e))

    def create(self):
        """Create a new {name.lower()}"""
        try:
            # Implementation needed
            return self.success(message="{name.title()} created successfully.")
        except Exception as e:
            return self.error(message=str(e))

    def show(self, id: int):
        """Get {name.lower()} by ID"""
        try:
            {name.lower()} = self.{name.lower()}_service.get_by_id(id)
            return self.success(content={name.lower()}, message="{name.title()} retrieved successfully.")
        except Exception as e:
            return self.error(message=str(e))

    def update(self, id: int):
        """Update {name.lower()}"""
        try:
            # Implementation needed
            return self.success(message="{name.title()} updated successfully.")
        except Exception as e:
            return self.error(message=str(e))

    def delete(self, id: int):
        """Delete {name.lower()}"""
        try:
            self.{name.lower()}_service.delete(id)
            return self.success(message="{name.title()} deleted successfully.")
        except Exception as e:
            return self.error(message=str(e))
'''
    else:
        template += f'''
        self.router.get("/", summary="Get {name.title()}", status_code=200)(self.index)

    def index(self):
        """Handle {name.lower()} requests"""
        try:
            return self.success(message="{name.title()} endpoint working!")
        except Exception as e:
            return self.error(message=str(e))
'''
    
    return template


def _generate_service_interface_template(name):
    """Generate service interface template"""
    return f'''from app.services.interfaces.i_service import IService

class I{name.title()}Service(IService):
    """Interface for {name.title()} service"""
    pass
'''


def _generate_service_implementation_template(name):
    """Generate service implementation template"""
    return f'''from app.core.decorators.di import service
from app.repositories.interfaces.{name.lower()}.i_{name.lower()}_repository import I{name.title()}Repository
from app.services.implements.service import Service
from app.services.interfaces.{name.lower()}.i_{name.lower()}_service import I{name.title()}Service

@service
class {name.title()}Service(Service, I{name.title()}Service):
    def __init__(self, repository: I{name.title()}Repository):
        # Update with appropriate response schema
        super().__init__(repository, None)  # Replace None with response schema class
'''


def _generate_repository_interface_template(name):
    """Generate repository interface template"""
    return f'''from app.repositories.interfaces.i_repository import IRepository

class I{name.title()}Repository(IRepository):
    """Interface for {name.title()} repository"""
    pass
'''


def _generate_repository_implementation_template(name):
    """Generate repository implementation template"""
    return f'''from app.core.decorators.di import infrastructure
from app.repositories.implements.repository import Repository
from app.repositories.interfaces.{name.lower()}.i_{name.lower()}_repository import I{name.title()}Repository
# from app.models.{name.lower()} import {name.title()}  # Uncomment when model exists

@infrastructure
class {name.title()}Repository(Repository, I{name.title()}Repository):
    def __init__(self):
        # Update with actual model class
        super().__init__(None)  # Replace None with model class
'''


def _generate_model_template(name, fields):
    """Generate model template"""
    template = f'''from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.models.abstract_model import AbstractModel

class {name.title()}(AbstractModel):
    __tablename__ = '{name.lower()}s'

'''
    
    if fields:
        for field in fields.split(','):
            if ':' in field:
                field_name, field_type = field.split(':')
                if field_type.lower() in ['str', 'string']:
                    template += f"    {field_name} = Column(String(255), nullable=False)\n"
                elif field_type.lower() in ['int', 'integer']:
                    template += f"    {field_name} = Column(Integer, nullable=False)\n"
                elif field_type.lower() in ['bool', 'boolean']:
                    template += f"    {field_name} = Column(Boolean, default=True)\n"
                else:
                    template += f"    {field_name} = Column(String(255), nullable=False)  # {field_type}\n"
    else:
        template += "    # Add your model fields here\n"
        template += "    # name = Column(String(100), nullable=False)\n"
    
    return template


def _generate_schema_template(name, schema_type):
    """Generate schema template"""
    if schema_type == 'response':
        return f'''from pydantic import BaseModel, ConfigDict

class {name.title()}ResponseSchema(BaseModel):
    """Response schema for {name.title()}"""
    id: int
    # Add response fields here
    
    model_config = ConfigDict(from_attributes=True)
'''
    elif schema_type == 'request':
        return f'''from pydantic import BaseModel

class {name.title()}RequestSchema(BaseModel):
    """Request schema for {name.title()}"""
    # Add request fields here
    pass
'''
    else:  # model
        return f'''from pydantic import BaseModel, ConfigDict

class {name.title()}BaseSchema(BaseModel):
    """Base schema for {name.title()}"""
    # Add base fields here
    
    model_config = ConfigDict(from_attributes=True)
'''


def _update_routes_registration(name):
    """Update routes registration in api.py"""
    routes_file = Path("app/routes/api.py")
    if routes_file.exists():
        click.echo(f"💡 Don't forget to register {name.title()}Controller in app/routes/api.py:")
        click.echo(f"   route_registrar.register({name.title()}Controller, \"/{name.lower()}\", [\"{name.title()}\"])")


if __name__ == '__main__':
    cli() 