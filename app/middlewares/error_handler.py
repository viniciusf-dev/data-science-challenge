from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.api_exceptions import APIException

def register_error_handlers(app):
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
        
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocorreu um erro interno."}
        )
