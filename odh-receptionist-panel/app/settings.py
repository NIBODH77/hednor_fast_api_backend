from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ------------------------
    # Project Info
    # ------------------------
    PROJECT_NAME: str = "ODH Receptionist Panel"
    DEBUG: bool = True

    # ------------------------
    # Database
    # ------------------------
    DATABASE_URL: str = "sqlite+aiosqlite:///./receptionist.db"

    # ------------------------
    # SMS Gateway (smsgateway.center)
    # ------------------------
    SMSGW_BASE_URL: str = "https://unify.smsgateway.center/SMSApi/send"
    SMSGW_USERID: str = "vprlst"
    SMSGW_PASSWORD: str = "Odh@87612"
    SMSGW_SENDERID: str = "ODHGRP"
    

    # ------------------------
    # DLT IDs
    # ------------------------
    DLT_ENTITY_ID: str | None = "3686"
    DLT_TEMPLATE_ID_OTP: str | None = "1707175239899941851"

    # ------------------------
    # Security
    # ------------------------
    SECRET_KEY: str = "logan"  # ⚠️ production में env से लीजिए
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"   # load values from .env
        case_sensitive = True


# ek global object
settings = Settings()

# dependency injection ke liye function
def get_settings() -> Settings:
    return settings