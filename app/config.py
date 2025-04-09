from pydantic import Field, validator
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = Field('user', env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field('password', env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field('restaurant_db', env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("db", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")

    @validator("POSTGRES_PORT", pre=True)
    def validate_postgres_port(cls, v):
        if v == "" or v is None:
            return 5432
        return int(v)

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    APP_HOST: str = Field("0.0.0.0", env="APP_HOST")
    APP_PORT: int = Field(8000, env="APP_PORT")
    DEBUG: bool = Field(False, env="DEBUG")

    @validator("APP_PORT", pre=True)
    def validate_app_port(cls, v):
        if v == "" or v is None:
            return 8000
        return int(v)

    @validator("DEBUG", pre=True)
    def validate_debug(cls, v):
        # Если передана строка, пытаемся интерпретировать её как булево значение
        if isinstance(v, str):
            if v.lower() in {"true", "1", "yes", "on"}:
                return True
            elif v.lower() in {"false", "0", "no", "off"}:
                return False
            else:
                return False
        return bool(v)

    BASE_DIR: str = Field(default_factory=lambda: str(Path(__file__).parent.parent.resolve()))
    ALEMBIC_CONFIG: str = Field("../alembic.ini", env="ALEMBIC_CONFIG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
