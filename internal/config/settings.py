import os
from typing import Any, Dict, List

from async_fastapi_jwt_auth import AuthJWT
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):

    API: str = '/api'
    RPC: str = '/rpc'
    DOCS: str = '/docs'
    ADMIN: str = '/admin'
    STARTUP: str = 'startup'
    SHUTDOWN: str = 'shutdown'
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    FLASK_ADMIN_SWATCH: str = 'cerulean'

    NAME: str = 'FastAPI Clean API'
    VERSION: str = '1.0'
    DESCRIPTION: str = 'FastAPI Clean REST API'

    SWAGGER_UI_PARAMETERS: Dict[str, Any] = {
        'displayRequestDuration': True,
        'filter': True,
    }

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(
            cls, value: str | List[str],  # noqa: N805, WPS110
    ) -> str | List[str]:
        if isinstance(value, str) and not value.startswith('['):
            return [i.strip() for i in value.split(',')]
        elif isinstance(value, (list, str)):
            return value

        raise ValueError(value)

    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")

    DATABASE_URI: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    authjwt_secret_key: str = os.getenv('AUTHJWT_SECRET_KEY')
    ACCESS_TOKEN_EXPIRES_IN: int = os.getenv('ACCESS_TOKEN_EXPIRES_IN')
    REFRESH_TOKEN_EXPIRES_IN: int = os.getenv('REFRESH_TOKEN_EXPIRES_IN')

    class Config:
        case_sensitive = True


settings = Settings()


@AuthJWT.load_config
def get_config():
    return Settings()

