from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Any

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.supabase import supabase
from app.schemas.user import User, UserCreate, UserInDB, UserRole, UserUpdate
from app.schemas.token import Token
from app.core.deps import get_current_admin_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate) -> Any:
    """
    Registra un nuevo usuario.
    """
    # verificar si el usuario ya existe 
    response = supabase.table("user_profiles").select("*").eq("email", user_in.email).execute()
    if response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado en la base de datos"
        )
    
    # crear usuario en Supabase 
    try:
        auth_response = supabase.auth.sign_up({
            "email": user_in.email,
            "password": user_in.password
        })
        user_id = auth_response.user.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al registrar usuario: {str(e)}"
        )
    
    
    user_data = {
        "full_name": user_in.full_name,
        "role": user_in.role.value,
        "is_active": user_in.is_active
    }
    
    try:
        # actualizar el perfil 
        response = supabase.table("user_profiles").update(user_data).eq("id", user_id).execute()
        return response.data[0]
    except Exception as e:
        
        user_data["id"] = user_id
        user_data["email"] = user_in.email
        response = supabase.table("user_profiles").insert(user_data).execute()
        return response.data[0]

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Obtiene un token de acceso para el usuario.
    """
    try:
        # login con Supabase
        response = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password
        })
        
        # crear token propio con JWT
        access_token = create_access_token(
            subject=response.user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)) -> Any:
    """
    Obtiene el usuario actual.
    """
    try:
        # Verificamos el token con Supabase
        user = supabase.auth.get_user(token)
        
        # Obtenemos datos del usuario 
        response = supabase.table("user_profiles").select("*").eq("id", user.user.id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/admin/create-user", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_admin_or_operator(
    user_in: UserCreate, 
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Crea un nuevo usuario con rol de administrador u operador.
    Solo los administradores pueden crear estos tipos de usuarios.
    """
    # verificar que el rol sea válido (admin u operator)
    if user_in.role not in [UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden crear usuarios con rol de administrador u operador"
        )
    
    # verificar si el usuario ya existe
    response = supabase.table("user_profiles").select("*").eq("email", user_in.email).execute()
    if response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado en la base de datos"
        )
    
    # crear usuario en 
    try:
        auth_response = supabase.auth.admin.create_user({
            "email": user_in.email,
            "password": user_in.password,
            "email_confirm": True,  # confirmar email automáticamente
            "user_metadata": {
                "name": user_in.full_name,
                "role": user_in.role.value
            }
        })
        user_id = auth_response.user.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al registrar usuario: {str(e)}"
        )
    
   
    user_data = {
        "full_name": user_in.full_name,
        "role": user_in.role.value,
        "is_active": user_in.is_active
    }
    
    try:
        response = supabase.table("user_profiles").update(user_data).eq("id", user_id).execute()
        return response.data[0]
    except Exception as e:
        
        user_data["id"] = user_id
        user_data["email"] = user_in.email
        response = supabase.table("user_profiles").insert(user_data).execute()
        return response.data[0]
    
    
@router.get("/admin/users", response_model=list[User])
async def list_users(
    current_user: User = Depends(get_current_admin_user),
    skip: int = 0,
    limit: int = 100
    ) -> Any:
        """
        Lista todos los usuarios (solo administradores)
        """
        try:
            
            response = supabase.table("user_profiles")\
                .select("*")\
                .range(skip, skip + limit - 1)\
                .order("created_at", desc=True)\
                .execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al listar usuarios: {str(e)}"
        )

@router.put("/admin/users/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Actualiza un usuario (solo administradores)
    """
    try:
        update_data = user_update.dict(exclude_unset=True)
        
        response = supabase.table("user_profiles")\
            .update(update_data)\
            .eq("id", user_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar usuario: {str(e)}"
        )