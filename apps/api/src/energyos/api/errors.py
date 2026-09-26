import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from energyos.domain.errors import EnergyOSError

logger = logging.getLogger(__name__)


def current_request_id(request: Request) -> str:
    request_id = getattr(request.state, "request_id", None)
    if isinstance(request_id, str) and request_id:
        return request_id
    header = request.headers.get("x-request-id", "").strip()
    return header or "unknown"


def public_validation_errors(exc: RequestValidationError) -> list[dict[str, str]]:
    published: list[dict[str, str]] = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error.get("loc", ()))
        published.append(
            {
                "location": location,
                "message": str(error.get("msg", "Invalid value")),
            }
        )
    return published


def error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    request_id: str,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "details": details or {},
            "request_id": request_id,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EnergyOSError)
    def handle_domain_error(request: Request, exc: EnergyOSError) -> JSONResponse:
        return error_response(
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
            request_id=current_request_id(request),
        )

    @app.exception_handler(RequestValidationError)
    def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return error_response(
            status_code=422,
            code="validation_error",
            message="Request validation failed",
            request_id=current_request_id(request),
            details={"errors": public_validation_errors(exc)},
        )

    @app.exception_handler(HTTPException)
    def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        code = "not_found" if exc.status_code == 404 else "http_error"
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return error_response(
            status_code=exc.status_code,
            code=code,
            message=message,
            request_id=current_request_id(request),
        )

    @app.exception_handler(Exception)
    def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled error request_id=%s error_type=%s",
            current_request_id(request),
            type(exc).__name__,
        )
        return error_response(
            status_code=500,
            code="internal_error",
            message="Unexpected server error",
            request_id=current_request_id(request),
        )
