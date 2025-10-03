from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = "sqlite:///./scores.db"

    # API externa
    API_URL: str= "http://scoring-api:9000/alerts"
    API_KEY: str = "XXX-YYY-ZZZ-1234"
    MAX_PER_PAGE: int = 20

    class Config:
        env_file = ".env"

# Instancia global que se importa en otros módulos
settings = Settings()
