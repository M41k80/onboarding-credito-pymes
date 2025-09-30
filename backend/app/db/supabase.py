from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """
    aqui se crea y devuelve un cliente de Supabase utilizando las credenciales configuradas.
    
    Returns:
        Client: Cliente de Supabase inicializado
    """
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    
    if not url or not key:
        raise ValueError("Las credenciales de Supabase no están configuradas correctamente")
    
    return create_client(url, key)

# Cliente global para reutilización
supabase = get_supabase_client()