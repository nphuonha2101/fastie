# Fastie - FastAPI Web Framework

Fastie là một framework web được xây dựng trên FastAPI với kiến trúc modular, áp dụng Clean Architecture patterns bao gồm Repository Pattern, Service Layer và Dependency Injection.

## 🚀 Tính năng hiện tại

- **API RESTful** với FastAPI framework
- **Quản lý người dùng cơ bản** (đăng ký, liệt kê users)  
- **Kiến trúc phân lớp** với Repository Pattern và Service Layer
- **Dependency Injection** với auto-discovery components
- **Database Migration** với Alembic
- **Schema Validation** với Pydantic và EmailStr
- **Soft Delete** support trong database models

## 🏗️ Kiến trúc Project

```
app/
├── api/v1/                    # API Controllers và Middlewares
│   ├── controllers/           # HTTP request handlers
│   │   ├── auth/             # Authentication endpoints
│   │   └── user_account/     # User management endpoints
│   └── middlewares/           # Custom middlewares
├── core/                      # Core framework functionality
│   ├── decorators/            # DI decorators (@controller, @service, etc.)
│   ├── providers/             # Application service providers
│   └── service_containers/    # IoC Container implementation
├── infrastructures/           # External services integration
│   └── database/              # Database connection và session management
├── models/                    # SQLAlchemy ORM models
├── repositories/              # Data access layer
│   ├── interfaces/            # Repository contracts
│   └── implements/            # Repository implementations
├── services/                  # Business logic layer
│   ├── interfaces/            # Service contracts  
│   └── implements/            # Service implementations
├── schemas/                   # Pydantic schemas
│   ├── models/                # Base schemas cho models
│   ├── requests/              # Request DTOs
│   └── responses/             # Response DTOs
└── routes/                    # Route registration
```

## 📋 Yêu cầu hệ thống

- **Python 3.8+**
- **Database**: MySQL/PostgreSQL/SQLite (hỗ trợ SQLAlchemy)
- **Package Manager**: pip hoặc poetry

## 🔧 Cài đặt và Setup

### 1. Clone repository
```bash
git clone <repository-url>
cd fastie
```

### 2. Setup Python environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình Environment
Tạo file `.env` trong thư mục root:
```env
# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/fastie_db

# Hoặc sử dụng SQLite cho development
# DATABASE_URL=sqlite:///./fastie.db
```

### 5. Database Migration
```bash
# Chạy migration hiện có
alembic upgrade head

# Tạo migration mới (nếu có thay đổi model)
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### 6. Chạy ứng dụng

#### Sử dụng Fastie CLI (Recommended)
```bash
# Chạy development server với auto-reload
python fastie.py serve --reload

# Chạy production server
python fastie.py serve --host 0.0.0.0 --port 8000
```

#### Sử dụng Uvicorn trực tiếp
```bash
# Development mode với auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Truy cập ứng dụng:**
- API: `http://localhost:8000`
- Interactive API Docs: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

## 📚 API Endpoints

### Authentication Routes (`/auth`)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| `POST` | `/auth/login` | User login | ⚠️ Mock implementation |
| `GET` | `/auth/greet` | Test endpoint | ✅ Working |

### User Management (`/user`)  
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/user/` | Lấy danh sách users | - | `List[UserResponseSchema]` |
| `POST` | `/user/register` | Đăng ký user mới | `UserCreateSchema` | `UserResponseSchema` |

## 🗃️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    avatar VARCHAR(255) NULL,
    token VARCHAR(255) NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME NULL  -- Soft delete support
);
```

### Pydantic Schemas

**UserCreateSchema:**
```python
{
    "name": "John Doe",
    "email": "john@example.com", 
    "password": "securepassword",
    "is_active": 1,
    "avatar": "https://example.com/avatar.jpg"
}
```

**UserResponseSchema:**
```python
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "is_active": 1,
    "avatar": "https://example.com/avatar.jpg"
    // password và token không được trả về
}
```

## 🔧 Database Migration

### Quản lý Migration

#### Sử dụng Fastie CLI
```bash
# Tạo migration mới
python fastie.py make migration create_posts_table --table posts

# Chạy migrations
python fastie.py db migrate

# Rollback migrations
python fastie.py db rollback --steps 2

# Reset database
python fastie.py db reset

# Xem status migrations
python fastie.py db status
```

#### Sử dụng Alembic trực tiếp
```bash
# Xem migration history
alembic history

# Xem current revision
alembic current

# Tạo migration mới khi có thay đổi model
alembic revision --autogenerate -m "Add new table"

# Upgrade to latest
alembic upgrade head

# Downgrade một bước
alembic downgrade -1

# Downgrade về revision cụ thể
alembic downgrade <revision_id>
```

## 🏗️ Dependency Injection System

Framework sử dụng decorator-based DI system với auto-discovery:

### Decorators
```python
@controller          # Đánh dấu class là Controller
@service            # Đánh dấu class là Service  
@infrastructure     # Đánh dấu class là Infrastructure
@inject             # Enable constructor injection
```

### Ví dụ sử dụng
```python
@controller
@inject
class UserAccountController(BaseController):
    def __init__(self, user_service: IUserService):
        self.user_service = user_service
```

## ⚡ Fastie CLI - Laravel Artisan cho Python

Fastie framework đi kèm với một CLI tool mạnh mẽ giống như Laravel Artisan để tự động hóa các tác vụ development.

### Khởi tạo Project mới
```bash
# Tạo project mới với MySQL
python fastie.py new my_project --database mysql

# Tạo project với SQLite
python fastie.py new my_project --database sqlite

# Tạo project với authentication boilerplate
python fastie.py new my_project --auth
```

### Database Commands
```bash
# Migration commands
python fastie.py db migrate          # Chạy migrations
python fastie.py db rollback         # Rollback 1 step
python fastie.py db rollback -s 3    # Rollback 3 steps
python fastie.py db reset            # Reset database
python fastie.py db status           # Xem migration status
```

### Code Generation Commands
```bash
# Tạo migration
python fastie.py make migration create_posts_table --table posts

# Tạo model
python fastie.py make model Post --fields "title:str,content:str,is_published:bool"

# Tạo controller
python fastie.py make controller Post                    # Simple controller
python fastie.py make controller Post --resource         # Resource controller với CRUD

# Tạo service
python fastie.py make service Post

# Tạo repository
python fastie.py make repository Post

# Tạo schema
python fastie.py make schema Post --type request         # Request schema
python fastie.py make schema Post --type response       # Response schema
python fastie.py make schema Post --type model          # Model schema
```

### Server Commands
```bash
# Start development server
python fastie.py serve --reload

# Start production server
python fastie.py serve --host 0.0.0.0 --port 8000

# Xem tất cả routes
python fastie.py routes
```

### Utility Commands
```bash
# Install dependencies
python fastie.py install

# Xem help
python fastie.py --help
python fastie.py make --help
python fastie.py db --help

# Chạy demo CLI
python demo.py

# Cleanup demo files
python cleanup_demo.py
```

### Workflow ví dụ - Tạo Blog Post feature
```bash
# 1. Tạo model và migration
python fastie.py make model Post --fields "title:str,content:str,slug:str,is_published:bool"
python fastie.py make migration create_posts_table --table posts

# 2. Tạo schemas
python fastie.py make schema Post --type request
python fastie.py make schema Post --type response

# 3. Tạo repository và service
python fastie.py make repository Post
python fastie.py make service Post

# 4. Tạo controller với CRUD methods
python fastie.py make controller Post --resource

# 5. Chạy migration
python fastie.py db:migrate

# 6. Start server
python fastie.py serve --reload
```

## 🛠️ Development Guide

### Thêm Controller/Endpoint mới

1. **Tạo Schema** (nếu cần):
```python
# schemas/requests/new_feature/
class NewFeatureCreateSchema(BaseModel):
    name: str
    description: str
```

2. **Tạo Repository Interface**:
```python
# repositories/interfaces/new_feature/
class INewFeatureRepository(IRepository):
    def find_by_name(self, name: str) -> Optional[NewFeature]:
        pass
```

3. **Implement Repository**:
```python
# repositories/implements/new_feature/
@infrastructure
class NewFeatureRepository(Repository, INewFeatureRepository):
    def find_by_name(self, name: str) -> Optional[NewFeature]:
        # Implementation
        pass
```

4. **Tạo Service Interface & Implementation**:
```python
# services/interfaces/new_feature/
class INewFeatureService(IService):
    pass

# services/implements/new_feature/
@service  
class NewFeatureService(Service, INewFeatureService):
    def __init__(self, repository: INewFeatureRepository):
        super().__init__(repository, NewFeatureResponseSchema)
```

5. **Tạo Controller**:
```python
# api/v1/controllers/new_feature/
@controller
@inject
class NewFeatureController(BaseController):
    def __init__(self, service: INewFeatureService):
        self.service = service
        
    def define_routes(self):
        self.router.get("/", summary="Get Features")(self.index)
        
    def index(self):
        return self.success(content=self.service.get_all())
```

6. **Đăng ký Route**:
```python
# routes/api.py
route_registrar.register(NewFeatureController, "/features", ["Features"])
```

### Code Standards

- **Type Hints**: Bắt buộc cho tất cả functions và methods
- **Docstrings**: Sử dụng cho public methods
- **Error Handling**: Sử dụng try-catch trong controllers và services
- **Naming Convention**: 
  - Classes: PascalCase
  - Methods/Variables: snake_case
  - Constants: UPPER_SNAKE_CASE
- **Layer Separation**: Tuân thủ dependency direction trong Clean Architecture

### Testing (TODO)

```bash
# Unit tests
pytest tests/unit/

# Integration tests  
pytest tests/integration/

# Coverage report
pytest --cov=app tests/
```

## 🚧 Roadmap

### Planned Features
- [ ] **JWT Authentication** implementation trong AuthController
- [ ] **Password Hashing** với bcrypt
- [ ] **User Profile Management** endpoints
- [ ] **Role-based Authorization** middleware
- [ ] **API Rate Limiting**
- [ ] **Logging System** integration
- [ ] **Unit & Integration Tests**
- [ ] **Docker Support**
- [ ] **API Versioning** strategy

### Known Issues
- `POST /auth/login` hiện tại chỉ return mock response
- Chưa có validation cho password strength
- Chưa implement authentication middleware

## 🤝 Contributing

1. Fork project này
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

### Contribution Guidelines
- Tuân thủ coding standards đã định
- Viết tests cho features mới
- Update documentation khi cần thiết
- Ensure all DI decorators được sử dụng đúng cách

## 📈 Performance Notes

- **Auto-discovery**: Tự động scan và import tất cả components khi khởi động
- **Connection Pooling**: SQLAlchemy engine có pool_pre_ping=True
- **Lazy Loading**: Components chỉ được khởi tạo khi cần thiết

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using FastAPI, SQLAlchemy, và Clean Architecture principles.** 