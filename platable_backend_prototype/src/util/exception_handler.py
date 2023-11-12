from starlette.requests import Request
from starlette.responses import JSONResponse
from src.util.exceptions import HttpException


class ExceptionHandler:
    def handle(self, _request: Request, exception: Exception) -> JSONResponse:
        if isinstance(exception, HttpException):
            return JSONResponse(
                content={"message": exception.message},
                status_code=exception.status,
            )

        return JSONResponse(
            content={"message": "Internal server error."},
            status_code=500,
        )
