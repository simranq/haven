# Import key components to make them easily accessible
from .database import Base, SessionLocal, engine
from .models import User
from .schemas import UserCreate, UserUpdate, User, Token
from .auth import get_password_hash, verify_password
from .crud import (create_user, get_user, get_users, 
                  update_user, delete_user)

# Optional: Package version
__version__ = "0.1.0"

# This makes the package executable components easily importable
__all__ = [
    'Base',
    'SessionLocal',
    'engine',
    'User',
    'UserCreate', 
    'UserUpdate',
    'Token',
    'get_password_hash',
    'verify_password',
    'create_user',
    'get_user',
    'get_users',
    'update_user',
    'delete_user'
]