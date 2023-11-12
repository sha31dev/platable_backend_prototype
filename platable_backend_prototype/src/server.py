from fastapi import FastAPI
from gunicorn.app.base import BaseApplication
from typing import List, Optional
from src.config import Config
from src.util.exception_handler import ExceptionHandler


class Server(BaseApplication):
    def __init__(
        self,
        config: Config = Config(),
        controllers: Optional[List[any]] = None,
        exception_handler: ExceptionHandler = ExceptionHandler(),
    ):
        self.__config = config
        self.__controllers = controllers if controllers else []

        self.__app = FastAPI()
        super().__init__()

        for controller in self.__controllers:
            self.__app.api_route(path=controller.path, methods=controller.methods)(controller.handle)

        self.__app.exception_handler(Exception)(exception_handler.handle)

    def init(self, parser, opts, args):
        pass

    def load_config(self):
        self.cfg.set("bind", f"{self.__config.host}:{self.__config.port}")
        self.cfg.set("workers", self.__config.workers)
        self.cfg.set("worker_class", self.__config.worker_class)
        self.cfg.set("worker_connections", self.__config.worker_connections)
        self.cfg.set("timeout", self.__config.timeout)
        self.cfg.set("keepalive", self.__config.keepalive)
        self.cfg.set("capture_output", self.__config.capture_output)

    def load(self):
        return self.__app
    
    def set_openapi(self, openapi_spec: dict):
        self.__app.openapi = lambda: openapi_spec

    def start(self):
        self.run()
