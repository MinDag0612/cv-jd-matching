import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse


from app.core.exceptions import AppException
from app.models.response import ErrorResponse

logger = logging.getLogger(__name__)

async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    response = ErrorResponse(
        code=exc.code,
        mess=exc.mess,
    )

    return JSONResponse(
        status_code=exc.code,
        content=response.model_dump(mode="json"),
    )
    

async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    response = ErrorResponse(
        code=exc.status_code,
        mess=str(exc.detail),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json"),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    response = ErrorResponse(
        code=422,
        mess="Request validation failed",
    )

    return JSONResponse(
        status_code=422,
        content=response.model_dump(mode="json"),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception("Unhandled application exception")

    response = ErrorResponse(
        code=500,
        mess="Internal server error",
    )

    return JSONResponse(
        status_code=500,
        content=response.model_dump(mode="json"),
    )