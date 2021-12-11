from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = '0.0.0.0'
    SERVER_PORT: int = 8000
    PROJECT_NAME: str = 'Telethon Basic API'


settings = Settings()
