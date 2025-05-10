import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from app import settings
from app.api.handlers import product_router, admin_router, frontend_router
from app.db.session import get_db

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True) #вырубить echo в проде

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

app = FastAPI()

# Templates and static files setup
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create uploads directory if it doesn't exist
os.makedirs("app/static/uploads", exist_ok=True)

main_api_router = APIRouter()

# Include all routers
main_api_router.include_router(frontend_router, tags=["frontend"])
main_api_router.include_router(product_router, tags=["products"])
main_api_router.include_router(admin_router, tags=["admin"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port = 8004)