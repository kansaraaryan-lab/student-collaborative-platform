from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Student Collaborative Platform API"
    app_version: str = "0.1.0"
    debug: bool = True

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "platform_user"
    postgres_password: str = "platform_password"
    postgres_db: str = "student_platform"

    google_client_id: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
