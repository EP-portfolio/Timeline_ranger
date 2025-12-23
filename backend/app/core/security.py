"""
Sécurité : hashage de mots de passe et JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe en clair contre un hash."""
    # Utiliser bcrypt directement pour éviter les problèmes de compatibilité avec passlib
    try:
        password_bytes = plain_password.encode('utf-8')
        # Tronquer à 72 bytes si nécessaire
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la vérification du mot de passe: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash un mot de passe avec bcrypt."""
    # Bcrypt limite les mots de passe à 72 bytes
    password_bytes = password.encode('utf-8')
    
    # Tronquer à 72 bytes si nécessaire
    if len(password_bytes) > 72:
        print(f"[WARN] Mot de passe trop long ({len(password_bytes)} bytes), troncature à 72 bytes")
        password_bytes = password_bytes[:72]
    
    # Générer le salt et hasher
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Retourner en string
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crée un token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Décode et vérifie un token JWT."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

