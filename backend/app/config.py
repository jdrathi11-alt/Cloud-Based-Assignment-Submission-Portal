from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Cloud-Based Assignment Submission Portal"
    environment: str = "local"
    secret_key: str = "change-me-in-local-only"
    access_token_expire_minutes: int = 120
    database_url: str = "sqlite:///./portal.db"
    storage_mode: str = "local"
    auth_mode: str = "local"
    local_upload_dir: str = "./uploads"
    max_upload_mb: int = 10
    allow_late_submissions: bool = True
    allow_teacher_signup: bool = True
    cors_origins: str = "http://localhost:5173"
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None
    supabase_bucket: str = "assignment-submissions"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings():
    return Settings()
