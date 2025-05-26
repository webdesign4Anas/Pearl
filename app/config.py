from pydantic_settings import BaseSettings
from fastapi_mail import ConnectionConfig
from pydantic import EmailStr
  # Explicitly load the .env file
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    wow:int
    # Email configuration - add these to your Settings class
    mail_username: EmailStr
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True

    class Config:
        env_file = ".env"

settings = Settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from.strip(),
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,  # Changed from MAIL_TLS
    MAIL_SSL_TLS=settings.mail_ssl_tls,    # Changed from MAIL_SSL
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs
)



