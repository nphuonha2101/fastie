# 🚀 Middleware Usage Guide - Hướng Dẫn Sử Dụng Middleware

> **File tổng hợp duy nhất** - Tất cả thông tin về middleware system

## 📚 **Tổng Quan**

Framework FastAPI này cung cấp hệ thống middleware mạnh mẽ và linh hoạt với:
- ✅ **Dependency Injection** tự động
- ✅ **Middleware Groups** để quản lý tập trung
- ✅ **Custom Middleware** dễ dàng mở rộng
- ✅ **Route-specific** middleware configuration
- ✅ **Request State** sharing giữa middleware và controller

---

## 🏗️ **Kiến Trúc Middleware**

```
app/api/v1/middlewares/
├── abstract_middleware.py         # Base class
├── middleware_manager.py          # Central manager
├── auth/
│   └── auth_middleware.py        # JWT Authentication
├── cors_middleware.py            # Cross-Origin Resource Sharing
├── logging_middleware.py         # Request/Response logging
├── rate_limit_middleware.py      # Rate limiting
├── versioning_middleware.py      # API versioning (custom)
├── validation_middleware.py      # Request validation (custom)
└── caching_middleware.py         # Response caching (custom)
```

---

## 🎯 **Middleware Có Sẵn**

| Middleware | Chức năng | Request State | Sử dụng |
|------------|-----------|---------------|---------|
| **AuthMiddleware** | JWT authentication | `user_id` | Protected routes |
| **CORSMiddleware** | Handle CORS headers | `cors_headers` | All routes |
| **LoggingMiddleware** | Log requests | `start_time` | All routes |
| **RateLimitMiddleware** | Limit request rate | `rate_limit_headers` | Public routes |
| **VersioningMiddleware** | API versioning | `api_version`, `version_headers` | Version-aware APIs |
| **ValidationMiddleware** | Request validation | `validation_passed`, `request_size` | Strict validation |
| **CachingMiddleware** | Response caching | `cache_status`, `cached_data` | Performance optimization |

---

## 🎛️ **Middleware Groups**

### **Built-in Groups:**
```python
MiddlewareGroup.BASIC               # CORS + Logging
MiddlewareGroup.SECURITY            # Auth + Rate Limiting  
MiddlewareGroup.PUBLIC              # CORS + Logging + Rate Limiting
MiddlewareGroup.PROTECTED           # PUBLIC + Auth
MiddlewareGroup.FULL               # All basic middleware
```

### **Custom Groups:**
```python
MiddlewareGroup.HIGH_PERFORMANCE    # CORS + Logging + Caching + Rate Limiting
MiddlewareGroup.STRICT_VALIDATION   # CORS + Validation + Logging + Rate Limiting + Auth
MiddlewareGroup.API_VERSIONED       # Versioning + CORS + Logging + Rate Limiting
```

---

## 🔧 **Cách Sử Dụng**

### **1. Route Types (Khuyến nghị - Đơn giản nhất)**

```python
# routes/api.py
def register_routes(app: FastAPI):
    route_registrar = RouteRegistrar(app)

    # Public API (không cần authentication)
    route_registrar.register(
        AuthController, 
        prefix="/auth", 
        tags=["Auth"],
        route_type="public"
    )
    
    # Protected API (cần authentication)
    route_registrar.register(
        UserController, 
        prefix="/user", 
        tags=["User"],
        route_type="protected"
    )
```

### **2. Middleware Groups**

```python
# High performance API với caching
route_registrar.register(
    PostController,
    prefix="/posts",
    tags=["Posts"],
    middleware=MiddlewareGroup.HIGH_PERFORMANCE
)

# API với validation nghiêm ngặt
route_registrar.register(
    PaymentController,
    prefix="/payments", 
    tags=["Payments"],
    middleware=MiddlewareGroup.STRICT_VALIDATION
)
```

### **3. Additional Custom Middleware**

```python
from app.api.v1.middlewares.validation_middleware import ValidationMiddleware

route_registrar.register(
    ProductController,
    prefix="/products",
    route_type="public",
    additional_middlewares=[ValidationMiddleware]
)
```

---

## 💻 **Sử Dụng Middleware Data trong Controller**

### **Basic Pattern:**

```python
from fastapi import Request

class UserController(BaseController):
    def get_profile(self, request: Request):
        # Safe access với fallback
        user_id = getattr(request.state, 'user_id', None)
        api_version = getattr(request.state, 'api_version', 'v1')
        
        # Conditional access
        if hasattr(request.state, 'rate_limit_headers'):
            rate_limit = request.state.rate_limit_headers
        
        # Business logic dựa trên middleware data
        if api_version == "v2":
            return self.success(content={"format": "enhanced"})
        else:
            return self.success(content={"format": "legacy"})
```

### **Complete Example:**

```python
def get_middleware_info(self, request: Request):
    middleware_data = {}
    
    # Authentication
    middleware_data['user_id'] = getattr(request.state, 'user_id', 'anonymous')
    
    # Versioning
    middleware_data['api_version'] = getattr(request.state, 'api_version', 'v1')
    
    # Caching
    middleware_data['cache_status'] = getattr(request.state, 'cache_status', 'bypass')
    
    # Rate limiting
    if hasattr(request.state, 'rate_limit_headers'):
        middleware_data['rate_limit'] = request.state.rate_limit_headers
    
    # Validation
    if hasattr(request.state, 'validation_passed'):
        middleware_data['validation'] = {
            'passed': request.state.validation_passed,
            'size': getattr(request.state, 'request_size', 0)
        }
    
    return self.success(content=middleware_data)
```

---

## 🔨 **Tạo Custom Middleware**

### **Step 1: Tạo Middleware Class**

```python
# app/api/v1/middlewares/my_custom_middleware.py
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request
from app.api.v1.middlewares.abstract_middleware import AbstractMiddleware
from app.core.decorators.di import component

@component
class MyCustomMiddleware(AbstractMiddleware):
    def __init__(self):
        self.config = "custom_config"
        
    async def handle(self, request: Request, credentials: HTTPAuthorizationCredentials = None):
        # Custom logic
        request.state.custom_data = "processed_value"
        
        # Optional: Return info
        return {"custom": "middleware_executed"}
```

### **Step 2: Đăng ký vào MiddlewareManager**

```python
# app/api/v1/middlewares/middleware_manager.py

# 1. Import
from app.api.v1.middlewares.my_custom_middleware import MyCustomMiddleware

# 2. Add to enum
class MiddlewareGroup(Enum):
    CUSTOM_GROUP = "custom_group"

# 3. Add to groups
self._middleware_groups = {
    MiddlewareGroup.CUSTOM_GROUP: [
        CORSMiddleware,
        MyCustomMiddleware,
        LoggingMiddleware
    ]
}
```

### **Step 3: Sử dụng**

```python
route_registrar.register(
    MyController,
    prefix="/custom",
    middleware=MiddlewareGroup.CUSTOM_GROUP
)
```

---

## 🧪 **Test & Debug**

### **Debug Controller Pattern:**

```python
class DebugController(BaseController):
    def debug_middleware(self, request: Request):
        debug_info = {
            'method': request.method,
            'path': request.url.path,
            'headers': dict(request.headers),
        }
        
        # All request state
        if hasattr(request, 'state'):
            debug_info['state'] = vars(request.state)
        
        return self.success(content=debug_info)
```

---

## ⚡ **Performance & Best Practices**

### **1. Middleware Order:**

```python
# Optimal order cho performance
[
    VersioningMiddleware,    # Quick version check
    CORSMiddleware,         # Handle preflight
    ValidationMiddleware,   # Validate early
    CachingMiddleware,      # Check cache before expensive ops
    RateLimitMiddleware,    # Limit before auth
    AuthMiddleware,         # Authentication
    LoggingMiddleware       # Log everything
]
```

### **2. Conditional Processing:**

```python
class SmartMiddleware(AbstractMiddleware):
    async def handle(self, request: Request, credentials=None):
        # Skip for health checks
        if request.url.path in ["/health", "/metrics"]:
            return {"status": "skipped"}
            
        # Full processing for business endpoints
        return await self.process_request(request)
```

### **3. Error Handling:**

```python
class SafeMiddleware(AbstractMiddleware):
    async def handle(self, request: Request, credentials=None):
        try:
            result = await self.process_request(request)
            request.state.middleware_success = True
            return result
        except Exception as e:
            # Log but don't break request flow
            logger.error(f"Middleware error: {e}")
            request.state.middleware_error = str(e)
            return {"error": "non_critical"}
```

---

## 🔒 **Security & Configuration**

### **Environment Variables:**

```bash
# .env
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
RATE_LIMIT_PER_HOUR=1000
CACHE_TTL_SECONDS=300
MAX_REQUEST_SIZE_MB=10
```

### **Production Configuration:**

```python
# auth_middleware.py
import os

class AuthMiddleware(AbstractMiddleware):
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY required in production")
        
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
```

---

## 💡 **Custom Middleware Ideas**

Dưới đây là các ý tưởng cho custom middleware:

### **SecurityMiddleware**
```python
@component
class SecurityMiddleware(AbstractMiddleware):
    async def handle(self, request: Request, credentials=None):
        # IP whitelist/blacklist
        # Bot detection
        # Suspicious pattern detection
        # Security headers injection
        pass
```

### **MetricsMiddleware**
```python
@component
class MetricsMiddleware(AbstractMiddleware):
    async def handle(self, request: Request, credentials=None):
        # Request/response time tracking
        # Endpoint usage analytics
        # Error rate monitoring
        # Business metrics collection
        pass
```

### **GeolocationMiddleware**
```python
@component
class GeolocationMiddleware(AbstractMiddleware):
    async def handle(self, request: Request, credentials=None):
        # IP to location mapping
        # Geo-based content delivery
        # Regional compliance checking
        # Location-based rate limiting
        pass
```

---

## 🚀 **Quick Start Templates**

### **Minimal Setup:**
```python
route_registrar.register(AuthController, "/auth", ["Auth"], route_type="public")
route_registrar.register(UserController, "/user", ["User"], route_type="protected")
```

### **High Performance:**
```python
route_registrar.register(
    APIController, 
    "/api", 
    ["API"], 
    middleware=MiddlewareGroup.HIGH_PERFORMANCE
)
```

### **Enterprise Security:**
```python
route_registrar.register(
    EnterpriseController,
    "/enterprise",
    ["Enterprise"],
    middleware=MiddlewareGroup.STRICT_VALIDATION
)
```

---

## 📊 **Route Type Mapping**

| Route Type | Middleware Applied | Use Case |
|------------|-------------------|----------|
| `"public"` | CORS + Logging + RateLimit | Public APIs, login |
| `"protected"` | PUBLIC + Auth | User data, profiles |
| `"admin"` | PROTECTED + Enhanced security | Admin operations |
| `"basic"` | CORS + Logging | Simple endpoints |

---

## 🎯 **Kết Luận**

Middleware system này cung cấp:

✅ **Flexibility** - Nhiều cách config middleware  
✅ **Scalability** - Dễ dàng thêm custom middleware  
✅ **Performance** - Thứ tự execution được tối ưu  
✅ **Security** - Built-in auth, validation, rate limiting  
✅ **Maintainability** - Quản lý tập trung  
✅ **Testability** - Debug và monitoring dễ dàng  

**Framework ready cho production với enterprise-grade middleware system!** 🚀

---

## 📞 **Quick Reference**

### **Import Pattern:**
```python
from app.api.v1.middlewares.middleware_manager import MiddlewareGroup
from app.api.v1.middlewares.validation_middleware import ValidationMiddleware
```

### **Register Pattern:**
```python
route_registrar.register(Controller, "/prefix", ["Tags"], route_type="protected")
```

### **Access Pattern:**
```python
user_id = getattr(request.state, 'user_id', None)
```

**Framework hoàn chính sẵn sàng sử dụng!** 🎉 