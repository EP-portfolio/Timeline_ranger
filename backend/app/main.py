"""
Application FastAPI principale
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.api.v1 import auth, games, actions, websocket
import traceback

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS - DOIT être avant les routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestionnaire d'exceptions global pour s'assurer que CORS fonctionne même en cas d'erreur
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire d'exceptions global pour garantir les en-têtes CORS."""
    error_detail = str(exc)
    if settings.DEBUG:
        error_detail += f"\n{traceback.format_exc()}"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Erreur interne du serveur",
            "error": error_detail if settings.DEBUG else "Une erreur est survenue"
        },
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true",
        }
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

