from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """
    esquema para el token de acceso
    """
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """
    esquema para el payload del token JWT
    """
    sub: Optional[str] = None