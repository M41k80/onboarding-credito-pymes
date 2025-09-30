from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """Roles de usuario en el sistema"""
    ADMIN = "admin"
    OPERATOR = "operator"
    CLIENT = "client"

class UserBase(BaseModel):
    """esquema base para usuarios"""
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.CLIENT
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """esquema para crear usuarios"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """esquema para actualizar usuarios"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    """esquema base para usuarios en la base de datos"""
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class User(UserInDBBase):
    """esquema para respuestas de usuario"""
    pass

class UserInDB(UserInDBBase):
    """esquema para usuarios en la base de datos con hash de contraseña"""
    hashed_password: str