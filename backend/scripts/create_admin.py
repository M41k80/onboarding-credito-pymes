"""
Script para actualizar un usuario existente a administrador
"""
import sys
import os
import argparse
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))


from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
    print("❌ Error: Variables SUPABASE_URL y SUPABASE_KEY no encontradas")
    sys.exit(1)

from supabase import create_client

def update_to_admin(email: str, full_name: str):
    """
    Actualiza un usuario existente a administrador
    """
    print(f"🎯 Actualizando usuario a administrador: {email}")
    
    try:
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Conectado a Supabase")
        
        
        user_response = supabase.table("user_profiles").select("*").eq("email", email).execute()
        
        if not user_response.data:
            print(f"❌ El usuario {email} no existe en user_profiles")
            return False
        
        user_data = user_response.data[0]
        user_id = user_data["id"]
        
        print(f"✅ Usuario encontrado: {user_id}")
        print(f"   Rol actual: {user_data.get('role', 'No definido')}")
        
        
        update_response = supabase.table("user_profiles").update({
            "full_name": full_name,
            "role": "admin"
        }).eq("id", user_id).execute()
        
        if update_response.data:
            print("✅ Usuario actualizado a administrador exitosamente")
            print(f"\n📋 DATOS ACTUALIZADOS:")
            print(f"   👤 Email: {email}")
            print(f"   👤 Nombre: {full_name}")
            print(f"   🔑 ID: {user_id}")
            print(f"   🎯 Nuevo rol: admin")
            print(f"   ✅ Estado: Activo")
            return True
        else:
            print("❌ Error actualizando usuario")
            return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Actualizar usuario a administrador")
    parser.add_argument("--email", required=True, help="Email del usuario a actualizar")
    parser.add_argument("--name", required=True, help="Nombre completo")
    
    args = parser.parse_args()
    
    print("🚀 Actualizando usuario a administrador...")
    print("=" * 50)
    
    if update_to_admin(args.email, args.name):
        print("=" * 50)
        print("🎉 ¡USUARIO ACTUALIZADO A ADMINISTRADOR!")
        print("💡 Ya puedes iniciar sesión con permisos de administrador")
        sys.exit(0)
    else:
        print("=" * 50)
        print("💥 Error actualizando usuario")
        sys.exit(1)