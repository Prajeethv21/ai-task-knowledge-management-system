from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Task & Knowledge System"
    api_prefix: str = "/api"
    secret_key: str = Field(default="change_me", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = "HS256"

    database_url: str = Field(
        default="mysql+pymysql://root:root%20123@localhost:3306/ai_task_db",
        alias="DATABASE_URL",
    )
    allow_sqlite_fallback: bool = Field(default=False, alias="ALLOW_SQLITE_FALLBACK")
    upload_dir: str = Field(default="./storage/uploads", alias="UPLOAD_DIR")
    vector_dir: str = Field(default="./storage/vectors", alias="VECTOR_DIR")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")

    model_config = SettingsConfigDict(env_file=".env", populate_by_name=True)


settings = Settings()
