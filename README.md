# Sierra Madre Auth

A comprehensive authentication SDK for Python applications that provides user registration, login, and token-based authentication with configurable security levels.

## Features

- **User Registration**: Secure user registration with email validation
- **User Login**: JWT-based authentication with password verification
- **Token Management**: JWT token generation and validation
- **Password Security**: Configurable password security levels (1-4)
- **Auto-confirmation**: Optional automatic user confirmation
- **Flask Integration**: Built-in Flask decorators for secure endpoints
- **Database Models**: SQLAlchemy models for user management

## Installation

```bash
pip install sierra-madre-auth
```

## Quick Start

### Basic Setup

```python
from sierra_madre_auth.config import get_auth_config
from sierra_madre_auth.register import register_user
from sierra_madre_auth.login import login_user
from sierra_madre_core.requests import handle_endpoint
from flask import Blueprint, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

# Create auth blueprint
auth_blueprint = Blueprint("auth", __name__)

# Configure authentication
password_hash_key = os.getenv("JWT_SECRET_KEY")
auth_config = get_auth_config({
    "password_hash_key": password_hash_key, 
    "autoconfirm_users": True
})

# Register endpoint
@auth_blueprint.route("/register", methods=["POST"])
@handle_endpoint()
def api_register_user():
    return register_user(auth_config)

# Login endpoint
@auth_blueprint.route("/login", methods=["POST"])
@handle_endpoint()
def api_login_user():
    return login_user(auth_config)

# Protected endpoint example
@auth_blueprint.route("/validate-token", methods=["GET"])
@auth_config.handle_secure_endpoint()
def validate_token():
    return jsonify({"message": "Token is valid"}), 200
```

### Configuration Options

The `AuthConfig` class supports various configuration options:

```python
auth_config = get_auth_config({
    "password_hash_key": "your-secret-key",
    "algorithm": "HS256",  # JWT algorithm
    "token_expiration_time_minutes": 60,
    "password_security_level": 3,  # 1-4 levels
    "password_min_length": 8,
    "autoconfirm_users": False
})
```

### Password Security Levels

- **Level 1**: No minimum requirements
- **Level 2**: At least one uppercase and one lowercase letter
- **Level 3**: At least one lowercase, one uppercase, and one number
- **Level 4**: At least one lowercase, one uppercase, one number, and one special character

## API Endpoints

### Register User

**POST** `/register`

Request body:
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

Response:
```json
{
    "message": "User registered successfully"
}
```

### Login User

**POST** `/login`

Request body:
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

Response:
```json
{
    "message": "User logged in successfully",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Protected Endpoints

Use the `@auth_config.handle_secure_endpoint()` decorator to protect routes:

```python
@auth_blueprint.route("/protected", methods=["GET"])
@auth_config.handle_secure_endpoint()
def protected_endpoint():
    # Access the authenticated user ID
    user_id = request.id_user
    return jsonify({"user_id": user_id, "message": "Access granted"})
```

## Database Models

The SDK includes a `Users` model for database integration:

```python
from sierra_madre_auth.models import Users

# User model fields:
# - user_id: UUID primary key
# - email: String (required)
# - password: Hashed string (required)
# - confirmed: Boolean (default: False)
```

## Error Handling

The SDK provides comprehensive error handling for common authentication scenarios:

- Invalid email format
- Password security requirements not met
- User not found
- Invalid password
- User not confirmed (when auto-confirmation is disabled)
- Invalid JWT tokens

## Dependencies

- `sierra-madre-core`: Core functionality and error handling
- `flask`: Web framework integration
- `sqlalchemy`: Database models
- `pydantic`: Data validation
- `pyjwt`: JWT token handling

## Environment Variables

Set the following environment variable:

```bash
JWT_SECRET_KEY=your-secret-key-here
```

## License

This project is licensed under the MIT License.