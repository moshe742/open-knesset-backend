from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key = 'oknesset#@@#'
    ENV = "development"
