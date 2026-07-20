from datetime import datetime, timezone
from typing import Any, Optional

from fastapi.responses import JSONResponse


def success_response(
    message: str = "Operation completed successfully.",
    data: Optional[Any] = None,
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data if data is not None else {},
            "errors": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


def error_response(
    message: str = "Request failed.",
    errors: Optional[Any] = None,
    status_code: int = 400,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )