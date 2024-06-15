import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from src.constants import MINUTE, WEEK

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

ADDRESS_EMAIL_SERVER = os.getenv("ADDRESS_EMAIL_SERVER")
PORT_EMAIL_SERVER = os.getenv("PORT_EMAIL_SERVER")
LOGIN_EMAIL_SERVER = os.getenv("LOGIN_EMAIL_SERVER")
PASSWORD_EMAIL_SERVER = os.getenv("PASSWORD_EMAIL_SERVER")

BASE_DIR = Path(__file__).parent.parent


class App(BaseModel):
    title: str = "Birthday notifications!"


class Database(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"

    access_token_expire_seconds: int = 15 * MINUTE
    refresh_token_expire_minutes: int = 1 * WEEK


class MailServer(BaseModel):
    host: str = ADDRESS_EMAIL_SERVER
    port: int = PORT_EMAIL_SERVER
    login: str = LOGIN_EMAIL_SERVER
    password: str = PASSWORD_EMAIL_SERVER


class Settings(BaseSettings):
    app: App = App()
    database: Database = Database()
    auth_jwt: AuthJWT = AuthJWT()
    mail_server: MailServer = MailServer()


settings: Settings = Settings()
