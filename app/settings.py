from zoneinfo import ZoneInfo

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

TIMEZONE = ZoneInfo("UTC")

# PROJECT
APP_NAME = config("APP_NAME", cast=str, default="favoriteproduct")
DEBUG = config("DEBUG", cast=bool, default=True)
ENVIRONMENT = config("ENVIRONMENT", cast=str, default="local")
PAGE_SIZE = config("PAGE_SIZE", cast=int, default=10)

DB_URL = config(
    "DB_URL",
    default="mongodb://user:pass@web_db/favoriteproduct?authSource=admin",
)
DB_URL_TEST = config(
    "DB_URL_TEST",
    default="mongodb://user:pass@localhost/"
    "favoriteproduct_test?authSource=admin",
)

CHALLENGE_API = config(
    "CHALLENGE_API",
    default="http://challenge-api.luizalabs.com/api",
)

# SECURITY
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="")
SECRET_ALGORITHM = config("SECRET_ALGORITHM", cast=str, default="HS256")
ACCESS_TOKEN_TYPE = config("ACESS_TOKEN_TYPE", cast=str, default="Bearer")
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    cast=int,
    default=5,
)
