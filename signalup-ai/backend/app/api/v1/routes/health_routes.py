from fastapi import APIRouter

from app.core.constants import ResponseMessage
from app.core.database import get_database
from app.core.responses import success_response, error_response

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check():
    return success_response(
        message=ResponseMessage.HEALTH_OK,
        data={
            "service": "SignalUp AI Backend",
            "status": "healthy",
        },
    )


@router.get("/database")
async def database_health_check():
    try:
        database = get_database()
        await database.command("ping")

        return success_response(
            message=ResponseMessage.DATABASE_OK,
            data={
                "database": database.name,
                "status": "connected",
            },
        )

    except Exception:
        return error_response(
            message=ResponseMessage.DATABASE_ERROR,
            errors=None,
            status_code=503,
        )