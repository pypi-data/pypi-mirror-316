import os
from pydantic import BaseModel


class CoreConfig(BaseModel):
    TITLE: str = "Pazer Core - Python"
    VERSION: str = "0.1.0"
    CROSS_ALLOW_CROSS: bool = False
    CROSS_ALLOW_ORIGINS: list | None = None
    CROSS_ALLOW_CREDENTIALS: bool = False
    CROSS_ALLOW_METHODS: list | None = None
    CROSS_ALLOW_HEADERS: list | None = None
    DATABASE_HOST: dict | None = None
    SESSION_HOST: dict | None = None

    @staticmethod
    def MODE() -> str:
        return os.getenv("MODE", "NoneMode")

    @staticmethod
    def DEBUG() -> bool:
        return os.getenv("DEBUG", "False") in ["True", "1", "true", True]

    @staticmethod
    def LOG_ENABLE() -> bool:
        return os.getenv("LOG_ENABLE", "False") in ["True", "1", "true", True]

    @staticmethod
    def LOG_PATH() -> str:
        return os.getenv("LOG_PATH", "./Logs/")
