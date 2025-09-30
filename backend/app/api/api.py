from fastapi import APIRouter

from app.api.endpoints import auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# aqui se agregarán las demas rutas conforme el proyecto cresca
# un pequeno ejemplo:
# api_router.include_router(credit.router, prefix="/credits", tags=["credits"])
