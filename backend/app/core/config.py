"""
Configuration de l'application FastAPI
"""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    """Configuration de l'application."""
    
    # Application
    APP_NAME: str = "Timeline Ranger API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database Supabase
    SUPABASE_HOST: str
    SUPABASE_DB: str = "postgres"
    SUPABASE_USER: str = "postgres"
    SUPABASE_PASSWORD: str
    SUPABASE_PORT: str = "6543"  # Port du Connection Pooler (recommandé pour production)
    # Alternative: "5432" pour connexion directe (nécessite whitelist IP dans Supabase)
    
    # JWT Authentication
    SECRET_KEY: str = "changez-moi-en-production-avec-une-cle-secrete-forte"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 heures
    
    # CORS - Peut être une liste ou une string séparée par des virgules
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    def get_cors_origins(self) -> list[str]:
        """Convertit CORS_ORIGINS en liste."""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return self.CORS_ORIGINS if isinstance(self.CORS_ORIGINS, list) else []
    
    # WebSocket
    WEBSOCKET_PING_INTERVAL: int = 25
    WEBSOCKET_PING_TIMEOUT: int = 10
    
    class Config:
        # Chercher .env à la racine du projet
        # backend/app/core/config.py -> backend/ -> racine/
        env_file = str(Path(__file__).resolve().parent.parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignorer les variables supplémentaires dans .env


settings = Settings()

