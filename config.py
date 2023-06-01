from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key = 'oknesset#@@#'
    ENV = "development"
    oknesset_db_host: str
    oknesset_db_port: int = 5432
    oknesset_db_name: str
    oknesset_db_user: str
    oknesset_db_password: str

    class Config:
        env_file = '.env'
