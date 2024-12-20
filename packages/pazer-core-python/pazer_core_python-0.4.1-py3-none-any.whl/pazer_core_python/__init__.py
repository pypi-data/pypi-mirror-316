from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pazer_database_python.Executor import Executor
from pazer_logger_python import Logger
from pazer_core_python.CoreConfig import CoreConfig


class Core:
    def __init__(self, config: CoreConfig = CoreConfig(), fetch: bool = False):
        self.config: CoreConfig = config
        Logger.system("[Application] -> Initializing [Start]")
        self.app: FastAPI = FastAPI()
        self.executor: Executor = Executor()
        if fetch:
            self.fetch()
        Logger.system("[Application] -> Initializing [End]")

    def fetch(self) -> None:
        Logger.system("[Application] -> Fetch [Start]")
        self.__setting_core()
        self.__setting_cross()
        self.__setting_executor()
        Logger.system("[Application] -> Fetch [End]")

    def __setting_executor(self) -> None:
        Logger.system("[Application] -> Executor Setting [Start]")
        self.executor.loads(
            databaseConfig=self.config.DATABASE_HOST or {},
            sessionConfig=self.config.SESSION_HOST or {}
        )
        self.__log_config("DATABASE_HOST", self.config.DATABASE_HOST)
        self.__log_config("SESSION_HOST", self.config.SESSION_HOST)
        Logger.system("[Application] -> Executor Setting [End]")

    def __setting_core(self) -> None:
        Logger.system("[Application] -> Core Setting [Start]")
        self.app.title = self.config.TITLE or "None Name"
        self.app.version = self.config.VERSION or "None Version"

        self.__log_setting("TITLE", self.config.TITLE, "None Name")
        self.__log_setting("VERSION", self.config.VERSION, "None Version")
        self.__log_setting("MODE", self.config.MODE(), "None Name")
        self.__log_boolean("DEBUG", self.config.DEBUG())
        self.__log_boolean("LOG_ENABLE", self.config.LOG_ENABLE())
        self.__log_setting("LOG_PATH", self.config.LOG_PATH(), "./Logs/")

        Logger.system("[Application] -> Core Setting [End]")

    def __setting_cross(self) -> None:
        Logger.system("[Application] -> Core Cross Setting [Start]")
        Logger.info(f"[Application] -> Core Cross: {'True' if self.config.CROSS_ALLOW_CROSS else 'False'}")
        if self.config.CROSS_ALLOW_CROSS:
            self.app.add_middleware(
                CORSMiddleware,  # type: ignore
                allow_origins=self.config.CROSS_ALLOW_ORIGINS or [],
                allow_credentials=self.config.CROSS_ALLOW_CREDENTIALS,
                allow_methods=self.config.CROSS_ALLOW_METHODS or [],
                allow_headers=self.config.CROSS_ALLOW_HEADERS or []
            )
            self.__log_setting("CROSS_ALLOW_ORIGINS", self.config.CROSS_ALLOW_ORIGINS, [])
            self.__log_boolean("CROSS_ALLOW_CREDENTIALS", self.config.CROSS_ALLOW_CREDENTIALS)
            self.__log_setting("CROSS_ALLOW_METHODS", self.config.CROSS_ALLOW_METHODS, [])
            self.__log_setting("CROSS_ALLOW_HEADERS", self.config.CROSS_ALLOW_HEADERS, [])
        Logger.system("[Application] -> Core Cross Setting [End]")

    @staticmethod
    def __log_config(key: str, config_value: dict | None) -> None:
        count = f"List[{len(config_value)}]" if config_value else "List[0]"
        Logger.info(f"[Application] -> Executor Setting -> {key}: {count}")

    @staticmethod
    def __log_setting(key: str, value: any, default: any) -> None:
        Logger.info(f"[Application] -> Core Setting -> {key}: {value if value else default}")

    @staticmethod
    def __log_boolean(key: str, value: bool) -> None:
        Logger.info(f"[Application] -> Core Setting -> {key}: {'True' if value else 'False'}")
