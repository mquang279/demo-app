import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    port: int = int(os.getenv("PORT", "8080"))
    app_version: str = os.getenv("APP_VERSION", "v3.0.0")
    service_name: str = os.getenv("SERVICE_NAME", "backend")


settings = Settings()
