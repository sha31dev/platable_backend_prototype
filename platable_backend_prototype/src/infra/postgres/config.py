class Config:
    def __init__(
        self,
        database: str,
        drivername: str,
        host: str,
        password: str,
        port: int,
        username: str,
        pool_size: int = 1,
    ):
        self.__database = database
        self.__drivername = drivername
        self.__host = host
        self.__password = password
        self.__port = port
        self.__username = username
        self.__pool_size = pool_size

    @property
    def database(self) -> str:
        return self.__database

    @property
    def drivername(self) -> str:
        return self.__drivername

    @property
    def host(self) -> str:
        return self.__host

    @property
    def password(self) -> str:
        return self.__password

    @property
    def pool_size(self) -> int:
        return self.__pool_size

    @property
    def port(self) -> int:
        return self.__port
    
    @property
    def username(self) -> str:
        return self.__username
