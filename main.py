from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Annotated

app = FastAPI(
    title="FastAPI Dependencies Demo",
    description="A demonstration of using Depends() for reusable logic",
    version="1.0.0"
)

# -------------------------------------------------------------------
# Example 1: Common Query Parameters (Basic Dependency)
# -------------------------------------------------------------------
async def common_parameters(skip: int = 0, limit: int = 100):
    """
    A dependency function that extracts and validates common query parameters.
    This could contain more complex logic like authentication, logging, etc.
    """
    # Validate that limit is reasonable
    if limit > 200:
        limit = 200  # Enforce a maximum limit
    
    # You could add logging, analytics, etc. here
    print(f"Processing request with skip={skip}, limit={limit}")
    
    return {"skip": skip, "limit": limit}

# Using the dependency in multiple endpoints
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    """
    Get a list of items with pagination.
    The commons parameter is automatically provided by the common_parameters dependency.
    """
    # Simulate fetching items from a database
    items = [{"id": i, "name": f"Item {i}"} for i in range(commons["skip"], commons["skip"] + commons["limit"])]
    return {"message": "Listing items", "params": commons, "items": items}

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    """
    Get a list of users with pagination.
    Reuses the same common_parameters dependency.
    """
    # Simulate fetching users from a database
    users = [{"id": i, "name": f"User {i}"} for i in range(commons["skip"], commons["skip"] + commons["limit"])]
    return {"message": "Listing users", "params": commons, "users": users}

# -------------------------------------------------------------------
# Example 2: Class-based Dependency
# -------------------------------------------------------------------
class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 50):
        self.skip = skip
        self.limit = min(limit, 100)  # Enforce maximum limit

@app.get("/products/")
async def read_products(pagination: PaginationParams = Depends()):
    """
    Using a class as a dependency. FastAPI will automatically instantiate it
    and resolve the parameters from the query string.
    """
    products = [{"id": i, "name": f"Product {i}"} for i in range(pagination.skip, pagination.skip + pagination.limit)]
    return {"message": "Listing products", "skip": pagination.skip, "limit": pagination.limit, "products": products}

# -------------------------------------------------------------------
# Example 3: Dependency with Validation Logic (FIXED)
# -------------------------------------------------------------------
async def verify_api_key(x_api_key: str = Header(...)):
    """
    A dependency that verifies an API key from the request header.
    This demonstrates how dependencies can be used for authentication.
    """
    valid_keys = ["secret-key-123", "test-key-456"]
    
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return {"api_key": x_api_key, "user_id": "user-123"}  # Could fetch user info from DB

@app.get("/secure-data/")
async def get_secure_data(auth: dict = Depends(verify_api_key)):
    """
    A secure endpoint that requires a valid API key.
    The verify_api_key dependency handles the authentication logic.
    """
    return {
        "message": "Access granted to secure data",
        "user_id": auth["user_id"],
        "data": ["secret1", "secret2", "secret3"]
    }

# -------------------------------------------------------------------
# Example 4: Nested Dependencies
# -------------------------------------------------------------------
async def get_db_connection():
    """Simulate getting a database connection"""
    print("Getting DB connection...")
    # In a real app, this would connect to your database
    return {"connection": "database_connection_123"}

async def get_user_service(db: dict = Depends(get_db_connection)):
    """A dependency that depends on another dependency"""
    print("Creating user service with DB connection...")
    return {"user_service": f"service_with_{db['connection']}"}

@app.get("/user-stats/")
async def get_user_stats(service: dict = Depends(get_user_service)):
    """An endpoint that uses a dependency with its own dependencies"""
    return {
        "message": "User statistics",
        "service_used": service["user_service"],
        "stats": {"active_users": 150, "new_users": 25}
    }

# -------------------------------------------------------------------
# Example 5: Using Annotated (Alternative approach)
# -------------------------------------------------------------------
async def verify_api_key_annotated(x_api_key: Annotated[str, Header()]):
    """
    Alternative implementation using Annotated for type hints with dependencies.
    """
    valid_keys = ["secret-key-123", "test-key-456"]
    
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return {"api_key": x_api_key, "user_id": "user-123"}

@app.get("/secure-data-annotated/")
async def get_secure_data_annotated(auth: dict = Depends(verify_api_key_annotated)):
    """
    Alternative secure endpoint using Annotated dependency.
    """
    return {
        "message": "Access granted to secure data (Annotated version)",
        "user_id": auth["user_id"],
        "data": ["annotated_secret1", "annotated_secret2"]
    }

# Root endpoint to test the application
@app.get("/")
async def root():
    return {
        "message": "FastAPI Dependencies Demo",
        "endpoints": [
            "/items/?skip=0&limit=10",
            "/users/?skip=5&limit=20", 
            "/products/?skip=10&limit=30",
            "/secure-data/ (requires X-API-Key header)",
            "/secure-data-annotated/ (requires X-API-Key header)",
            "/user-stats/"
        ],
        "docs": "/docs"
    }
