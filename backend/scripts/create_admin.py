"""
Script para crear el primer usuario administrador en el sistema.
Uso: python create_admin.py --email admin@example.com --password securepassword --name "Nombre Completo"
"""
import sys
import os
import argparse
from pathlib import Path

# AGREGAR ESTO AL INICIO - Cargar variables de entorno PRIMERO
sys.path.append(str(Path(__file__).parent.parent))

# Cargar .env manualmente antes de cualquier import
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Verificar que las variables críticas estén cargadas
if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
    print("❌ Error: Variables SUPABASE_URL y SUPABASE_KEY no encontradas")
    print("   Asegúrate de tener un archivo .env en la raíz del proyecto")
    sys.exit(1)

# AHORA importar las dependencias que usan config
from app.db.supabase import get_supabase_client
from app.schemas.user import UserRole

def create_admin_user(email: str, password: str, full_name: str):
    """
    Crea un usuario administrador en Supabase.
    """
    print(f"Creando usuario administrador: {email}")
    
    try:
        # Inicializar cliente de Supabase
        supabase = get_supabase_client()
        
        # Verificar si el usuario ya existe
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            print(f"El usuario {email} ya existe en la base de datos.")
            return False
        
        # Crear usuario en Supabase Auth
        try:
            auth_response = supabase.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True,  # Confirmar email automáticamente
                "user_metadata": {"name": full_name}  # Agregar metadata
            })
            
            if hasattr(auth_response, 'user') and auth_response.user:
                user_id = auth_response.user.id
                print(f"Usuario creado en Supabase Auth con ID: {user_id}")
            else:
                print(f"Error: Respuesta de auth inesperada: {auth_response}")
                return False
                
        except Exception as e:
            print(f"Error al crear usuario en Supabase Auth: {str(e)}")
            return False
        
        # Incluir registro en la tabla users
        user_data = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "role": UserRole.ADMIN.value,
            "is_active": True
        }
        
        response = supabase.table("users").insert(user_data).execute()
        
        if response.data:
            print(f"✅ Usuario administrador creado exitosamente: {email}")
            print(f"   ID: {user_id}")
            print(f"   Nombre: {full_name}")
            print(f"   Rol: {UserRole.ADMIN.value}")
            return True
        else:
            print(f"Error al insertar en tabla users: {response}")
            return False
            
    except Exception as e:
        print(f"Error al crear usuario administrador: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Crear usuario administrador")
    parser.add_argument("--email", required=True, help="Correo electrónico del administrador")
    parser.add_argument("--password", required=True, help="Contraseña del administrador")
    parser.add_argument("--name", required=True, help="Nombre completo del administrador")
    
    args = parser.parse_args()
    
    success = create_admin_user(args.email, args.password, args.name)
    if success:
        print("🎉 Usuario administrador creado exitosamente.")
        sys.exit(0)
    else:
        print("💥 Error al crear usuario administrador.")
        sys.exit(1)

if __name__ == "__main__":
    main()