"""
Application FastAPI principale
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, games, actions, websocket

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(games.router, prefix="/api/v1")
app.include_router(actions.router, prefix="/api/v1")
app.include_router(websocket.router)


@app.get("/")
async def root():
    """Route racine."""
    return {
        "message": "Timeline Ranger API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Vérification de santé de l'API."""
    return {"status": "healthy"}


@app.on_event("shutdown")
async def shutdown():
    """Fermeture propre de l'application."""
    from app.core.database import Database
    Database.close()

