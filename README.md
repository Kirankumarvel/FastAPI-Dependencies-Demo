# FastAPI Dependencies Demo

This project demonstrates the power of FastAPI's dependency injection system using the `Depends()` function. Dependencies allow you to create reusable components for common tasks like parameter validation, authentication, database connections, and more.

---

## 🚀 Features

- **Common Parameter Handling**: Reuse pagination logic across multiple endpoints.
- **Class-based Dependencies**: Use classes as dependencies with automatic parameter resolution.
- **Authentication**: Implement API key validation as a reusable dependency.
- **Nested Dependencies**: Create dependencies that depend on other dependencies.
- **Automatic Documentation**: All dependencies are automatically documented in the interactive API docs.

---

## 📁 Project Structure

```
fastapi-dependencies-demo/
├── requirements.txt      # Project dependencies
├── .gitignore           # Git ignore rules
└── app/
    ├── __init__.py      # Makes app a Python package
    └── main.py          # Main application with dependency examples
```

---

## 🛠️ Installation & Setup

1. **Create and activate a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:

    ```bash
    uvicorn app.main:app --reload
    ```

4. **Open the interactive documentation**:
    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🎯 Key Concepts Demonstrated

### 1. Basic Function Dependency

The `common_parameters` function demonstrates how to extract and validate common query parameters across multiple endpoints:

```python
async def common_parameters(skip: int = 0, limit: int = 100):
    if limit > 200:
        limit = 200  # Business logic
    return {"skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"params": commons}
```

### 2. Class-based Dependency

Classes can also be used as dependencies:

```python
class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 50):
        self.skip = skip
        self.limit = min(limit, 100)

@app.get("/products/")
async def read_products(pagination: PaginationParams = Depends()):
    # FastAPI automatically instantiates the class with query parameters
```

### 3. Authentication Dependency

Dependencies are perfect for authentication and authorization:

```python
async def verify_api_key(x_api_key: str = Depends()):
    if x_api_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"user_id": "user-123"}

@app.get("/secure-data/")
async def get_secure_data(auth: dict = Depends(verify_api_key)):
    return {"data": "secure information"}
```

### 4. Nested Dependencies

Dependencies can depend on other dependencies:

```python
async def get_db_connection():
    return {"connection": "db_conn_123"}

async def get_user_service(db: dict = Depends(get_db_connection)):
    return {"user_service": f"service_with_{db['connection']}"}

@app.get("/user-stats/")
async def get_user_stats(service: dict = Depends(get_user_service)):
    return {"stats": "user statistics"}
```

---

## 🔍 How Dependencies Work

1. **Request Arrives:** FastAPI receives an HTTP request.
2. **Dependency Resolution:** FastAPI identifies all dependencies for the endpoint.
3. **Execution:** Each dependency function is executed in order.
4. **Result Injection:** The results are injected as parameters into your endpoint function.
5. **Endpoint Execution:** Your main endpoint function runs with all dependencies resolved.

---

## 📋 API Endpoints

| Endpoint        | Method | Description                               | Parameters         |
|-----------------|--------|-------------------------------------------|--------------------|
| `/`             | GET    | Welcome message with available endpoints  | -                  |
| `/items/`       | GET    | Get items with pagination                 | `skip`, `limit`    |
| `/users/`       | GET    | Get users with pagination                 | `skip`, `limit`    |
| `/products/`    | GET    | Get products with pagination              | `skip`, `limit`    |
| `/secure-data/` | GET    | Get secure data (requires API key)        | Header: `X-API-Key`|
| `/user-stats/`  | GET    | Get user statistics                       | -                  |

---

## 🔐 Testing the Secure Endpoint

To test `/secure-data/`, you need a valid API key in the header:

**Using curl**:
```bash
curl -H "X-API-Key: secret-key-123" http://127.0.0.1:8000/secure-data/
```

**Using the interactive docs**:
1. Go to http://127.0.0.1:8000/docs
2. Find `/secure-data/`
3. Click "Try it out"
4. Add header: Key `X-API-Key`, Value `secret-key-123`
5. Click "Execute"

**Valid API Keys** (defined in the code):
- `secret-key-123`
- `test-key-456`

---

## 🎓 Benefits of Using Dependencies

1. **Code Reuse:** Write logic once, use everywhere.
2. **Separation of Concerns:** Keep endpoint logic clean and focused.
3. **Testability:** Dependencies can be easily mocked during testing.
4. **Automatic Documentation:** FastAPI automatically documents all dependencies.
5. **Dependency Chains:** Create complex dependency trees resolved automatically.

---

## 🚨 Common Issues & Solutions

### Issue: `Depends()` not working
- **Solution:** Ensure you're importing `Depends` from `fastapi` and using it as a default parameter value.

### Issue: Dependency parameters not showing in docs
- **Solution:** Make sure your dependency function uses type hints for all parameters.

### Issue: Circular dependencies
- **Solution:** Restructure your code to avoid circular imports between dependencies.

---

## 📚 Next Steps

- Add database integration with SQLAlchemy
- Implement JWT token authentication
- Add request/response logging as a dependency
- Create rate limiting dependencies
- Add caching dependencies

Explore the official [FastAPI Dependencies Documentation](https://fastapi.tiangolo.com/tutorial/dependencies/) for more advanced patterns!

---
