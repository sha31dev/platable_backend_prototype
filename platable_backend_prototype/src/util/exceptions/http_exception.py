class HttpException(Exception):
    def __init__(self, status: int, message: str):
        self.__status = status
        self.__message = message
        super().__init__(self.__message)

    @property
    def status(self) -> int:
        return self.__status

    @property
    def message(self) -> str:
        return self.__message
