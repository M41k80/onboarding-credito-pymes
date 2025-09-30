from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    """Roles de usuario en el sistema de onboarding de creditos para PYMES """
    ADMIN = "admin"
    OPERATOR = "operator"
    CLIENT = "client"

class User:
    """
    este es el modelo de usuario para interactuar con la tabla de usuarios en Supabase.
    """
    def __init__(
        self,
        id: UUID,
        email: str,
        full_name: str,
        role: UserRole = UserRole.CLIENT,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.email = email
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        aqui se crea una instancia de User a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del usuario
            
        Returns:
            User: Instancia de User
        """
        return cls(
            id=data.get("id"),
            email=data.get("email"),
            full_name=data.get("full_name"),
            role=UserRole(data.get("role", UserRole.CLIENT)),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def to_dict(self) -> dict:
        """
        aqui se convierte la instancia de User a un diccionario.
        
        Returns:
            dict: Diccionario con los datos del usuario
        """
        return {
            "id": str(self.id) if self.id else None,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }