from envparse import Env


env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default= "postgresql+asyncpg://postgres:postgres@localhost:5435/altay_shop_db",
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

ALGORITHM = "HS256"
SECRET_KEY = "secret_key"