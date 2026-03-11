import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


class Settings(BaseSettings):
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST", default="localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", default=5432))

    INITIALIZE_SECRET_KEY: str = os.getenv("SECRET_KEY", default="supersecretkey")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRY_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    ALGORITHM: str = os.getenv("ALGORITHM")

    DATABASE_URL: str = (
        f"postgresql+psycopg2://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    class Config:
        env_file = ".env"


settings = Settings()
