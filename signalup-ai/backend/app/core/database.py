from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.core.logging import app_logger


class MongoDB:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongodb = MongoDB()


async def connect_to_mongo() -> None:
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGODB_URI)
        mongodb.database = mongodb.client[settings.MONGODB_DB_NAME]

        await mongodb.client.admin.command("ping")
        await create_indexes()

        app_logger.info("MongoDB connected successfully.")

    except Exception as exc:
        app_logger.exception(f"MongoDB connection failed: {str(exc)}")
        raise


async def close_mongo_connection() -> None:
    try:
        if mongodb.client:
            mongodb.client.close()
            app_logger.info("MongoDB connection closed.")
    except Exception as exc:
        app_logger.exception(f"MongoDB close connection failed: {str(exc)}")


def get_database() -> AsyncIOMotorDatabase:
    if mongodb.database is None:
        raise RuntimeError("Database is not initialized.")
    return mongodb.database


async def create_indexes() -> None:
    db = get_database()

    await db.users.create_index("email", unique=True)
    await db.users.create_index([("tenant_id", 1), ("status", 1)])
    await db.users.create_index([("tenant_id", 1), ("email", 1)])

    await db.roles.create_index([("tenant_id", 1), ("role_name", 1)], unique=True)

    await db.permissions.create_index("permission_name", unique=True)

    await db.refresh_tokens.create_index("token_hash", unique=True)
    await db.refresh_tokens.create_index([("tenant_id", 1), ("user_id", 1)])