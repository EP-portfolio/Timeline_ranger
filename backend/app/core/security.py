"""
Sécurité : hashage de mots de passe et JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Contexte pour le hashage des mots de passe
# Utiliser bcrypt directement pour éviter les problèmes de compatibilité avec passlib
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",  # Utiliser l'identifiant 2b (plus récent)
    bcrypt__rounds=12,  # Nombre de rounds
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe en clair contre un hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash un mot de passe."""
    # Log pour debug
    password_len = len(password) if password else 0
    password_bytes_len = len(password.encode('utf-8')) if password else 0
    print(f"[DEBUG] Hash password - longueur: {password_len} caractères, {password_bytes_len} bytes")
    
    # Bcrypt limite les mots de passe à 72 bytes
    # Tronquer si nécessaire (en bytes, pas en caractères)
    if password:
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            print(f"[WARN] Mot de passe trop long ({len(password_bytes)} bytes), troncature à 72 bytes")
            password_bytes = password_bytes[:72]
            password = password_bytes.decode('utf-8', errors='ignore')
    
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        error_msg = str(e)
        print(f"[ERREUR] Erreur lors du hashage: {error_msg}")
        # Si l'erreur mentionne 72 bytes, forcer la troncature
        if "72 bytes" in error_msg or "longer than" in error_msg.lower():
            if password:
                password_bytes = password.encode('utf-8')[:72]
                password = password_bytes.decode('utf-8', errors='ignore')
                print(f"[DEBUG] Nouvelle tentative avec mot de passe tronqué: {len(password.encode('utf-8'))} bytes")
                return pwd_context.hash(password)
        raise


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

