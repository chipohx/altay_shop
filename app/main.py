import uvicorn
from fastapi import FastAPI, APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app import settings
from app.api.handlers import product_router

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True) #вырубить echo в проде

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(product_router, prefix="/products", tags=["products"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port = 8004)