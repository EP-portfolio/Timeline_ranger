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
    import traceback
    error_detail = str(exc)
    error_traceback = traceback.format_exc()
    
    # Log l'erreur pour debug
    print(f"[ERREUR GLOBALE] {error_detail}")
    if settings.DEBUG:
        print(f"[TRACEBACK] {error_traceback}")
    
    # Déterminer l'origine autorisée
    origin = request.headers.get("origin")
    allowed_origins = settings.get_cors_origins()
    
    # Si l'origine est dans la liste autorisée, l'utiliser, sinon utiliser la première
    if origin and origin in allowed_origins:
        allow_origin = origin
    elif allowed_origins:
        allow_origin = allowed_origins[0]
    else:
        allow_origin = "*"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Erreur interne du serveur",
            "error": error_detail if settings.DEBUG else "Une erreur est survenue",
            "traceback": error_traceback if settings.DEBUG else None
        },
        headers={
            "Access-Control-Allow-Origin": allow_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
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


@app.get("/health/db")
async def health_check_db():
    """Vérification de la connexion à la base de données."""
    try:
        from app.core.database import Database
        with Database.get_cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
            return {
                "status": "healthy",
                "database": "connected",
                "host": settings.SUPABASE_HOST,
                "port": settings.SUPABASE_PORT
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "host": settings.SUPABASE_HOST,
            "port": settings.SUPABASE_PORT
        }


@app.on_event("shutdown")
async def shutdown():
    """Fermeture propre de l'application."""
    from app.core.database import Database
    Database.close()

