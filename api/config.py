from starlette.config import Config
from starlette.datastructures import Secret
env = Config(".env")

DATABASE_URL = env("DATABASE_URL", cast=Secret)
DATABASE_URL_TEST = env("DATABASE_URL_TEST", cast=Secret)

SECRET_KEY = env("SECRET_KEY", cast=Secret)
API_V1_STR = "/api/v1"
ACCESS_TOKEN_EXPIRE_MINUTES=30  