import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from auth import settings
from auth.api.handlers import auth_router

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

app = FastAPI(title="Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8003", "http://127.0.0.1:8003"],  # Main app URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates and static files setup
templates = Jinja2Templates(directory="auth/templates")
app.mount("/static", StaticFiles(directory="auth/static"), name="static")

main_api_router = APIRouter()

# Include auth router
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(main_api_router)

@app.get("/auth/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/auth/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 