import os
from dotenv import load_dotenv


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


DB_DRIVER = get_required_env("DB_DRIVER")
DB_USER = get_required_env("DB_USER")
DB_PASSWORD = get_required_env("DB_PASSWORD")
DB_HOST = get_required_env("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = get_required_env("DB_NAME")
SECRET_KEY= get_required_env('SECRET_KEY')
ALGORITHM= get_required_env('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_required_env("ACCESS_TOKEN_EXPIRE_MINUTES"))
