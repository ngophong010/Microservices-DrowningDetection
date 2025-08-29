from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE_NAME: str = "drowning_detection_db"
    PROJECT_NAME: str = "Drowning Detection API"
    SECRET_KEY: str # Can be generated with `openssl rand -hex 32`
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
