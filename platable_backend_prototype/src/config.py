class Config:
    def __init__(
        self,
        host: str = "0.0.0.0",
        keepalive: int = 86400,
        port: int = 5000,
        workers: int = 1,
        worker_class: str = "uvicorn.workers.UvicornWorker",
        worker_connections: int = 1024,
        timeout: int = 180,
        capture_output: bool = True,
    ):
        self.__host = host
        self.__keepalive = int(keepalive)
        self.__port = int(port)
        self.__workers = int(workers)
        self.__worker_class = worker_class
        self.__worker_connections = int(worker_connections)
        self.__timeout = int(timeout)
        self.__capture_output = capture_output

    @property
    def capture_output(self) -> bool:
        return self.__capture_output

    @property
    def host(self) -> str:
        return self.__host

    @property
    def keepalive(self) -> int:
        return self.__keepalive

    @property
    def port(self) -> int:
        return self.__port

    @property
    def workers(self) -> int:
        return self.__workers

    @property
    def worker_class(self) -> str:
        return self.__worker_class

    @property
    def worker_connections(self) -> int:
        return self.__worker_connections

    @property
    def timeout(self) -> int:
        return self.__timeout
