from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    DEEPGRAM_API_KEY: str
    GEMINI_API_KEY: str
    REDIS_BROKER: str
    REDIS_BACKEND: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()