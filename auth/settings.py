from email.policy import default

from envparse import Env
import os
from datetime import timedelta

env = Env()

REAL_DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5436/auth_db"
)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# JWT settings
JWT_SECRET_KEY = SECRET_KEY
JWT_ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 