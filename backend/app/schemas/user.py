"""
Schémas Pydantic pour les utilisateurs
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Schéma de base pour un utilisateur."""
    email: EmailStr
    username: Optional[str] = None


class UserCreate(UserBase):
    """Schéma pour créer un utilisateur."""
    password: str


class UserLogin(BaseModel):
    """Schéma pour la connexion."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schéma de réponse pour un utilisateur."""
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schéma pour le token JWT."""
    access_token: str
    token_type: str = "bearer"
    user: Optional[UserResponse] = None


class TokenData(BaseModel):
    """Données du token."""
    user_id: Optional[int] = None
    email: Optional[str] = None

