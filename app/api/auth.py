from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import httpx
from typing import Optional, Dict

# URL auth сервиса
AUTH_SERVICE_URL = "http://localhost:8001"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH_SERVICE_URL}/auth/token")

async def verify_token(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Проверяет токен через auth сервис
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/auth/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Зависимость для защищенных маршрутов
async def get_current_user(user_data: Dict = Depends(verify_token)) -> Dict:
    """
    Получает данные текущего пользователя
    """
    return user_data 