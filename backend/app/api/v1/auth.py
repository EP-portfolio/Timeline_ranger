"""
Routes d'authentification
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.models.user import UserModel
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from datetime import timedelta
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user_from_token(token: str) -> dict:
    """Fonction utilitaire pour obtenir l'utilisateur depuis un token (pour WebSockets)."""
    payload = decode_access_token(token)
    if payload is None:
        raise ValueError("Token invalide ou expiré")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise ValueError("Token invalide")
    
    user = UserModel.get_by_id(int(user_id))
    if user is None:
        raise ValueError("Utilisateur non trouvé")
    
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Dépendance pour obtenir l'utilisateur actuel depuis le token."""
    return get_current_user_from_token(token)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Inscription d'un nouvel utilisateur."""
    try:
        # Vérifier si l'email existe déjà
        existing_user = UserModel.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la vérification de l'email : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de connexion à la base de données : {str(e)}"
        )
    
    try:
        # Créer l'utilisateur
        password_hash = get_password_hash(user_data.password)
        user = UserModel.create(
            email=user_data.email,
            password_hash=password_hash,
            username=user_data.username
        )
        return user
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la création de l'utilisateur : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'inscription : {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Connexion d'un utilisateur."""
    try:
        user = UserModel.get_by_email(form_data.username)  # OAuth2 utilise 'username' pour l'email
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la récupération de l'utilisateur : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de connexion à la base de données : {str(e)}"
        )
    
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Mettre à jour la dernière connexion
        UserModel.update_last_login(user["id"])
        
        # Créer le token
        access_token = create_access_token(
            data={"sub": str(user["id"]), "email": user["email"]}
        )
        
        # Retirer le password_hash de la réponse
        user_response = {k: v for k, v in user.items() if k != "password_hash"}
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_response
        }
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la création du token : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la connexion : {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Récupère les informations de l'utilisateur connecté."""
    # Retirer le password_hash de la réponse
    current_user.pop("password_hash", None)
    return current_user

