from pydantic_settings import BaseSettings
from pydantic import Field

# CONFIGURE ENVIRONMENT VARIABLES
class Settings(BaseSettings):
    database_hostname :str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    alembic_password:str

    class Config:
        env_file =".env"



settings = Settings()
