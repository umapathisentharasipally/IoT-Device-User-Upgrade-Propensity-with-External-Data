from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.utils.object_id import validate_object_id


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.users
        self.refresh_tokens = db.refresh_tokens

    async def create(self, user_data: dict) -> dict:
        user_data["created_at"] = datetime.now(timezone.utc)
        user_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.insert_one(user_data)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get_by_email(self, email: str) -> dict | None:
        return await self.collection.find_one({"email": email.lower()})

    async def get_by_id(self, user_id: str, tenant_id: str) -> dict | None:
        return await self.collection.find_one(
            {
                "_id": validate_object_id(user_id),
                "tenant_id": tenant_id,
                "is_deleted": False,
            }
        )

    async def list_users(self, tenant_id: str, skip: int = 0, limit: int = 20) -> list[dict]:
        cursor = (
            self.collection.find({"tenant_id": tenant_id, "is_deleted": False})
            .skip(skip)
            .limit(limit)
            .sort("created_at", -1)
        )
        return await cursor.to_list(length=limit)

    async def update(self, user_id: str, tenant_id: str, update_data: dict) -> dict | None:
        update_data["updated_at"] = datetime.now(timezone.utc)

        await self.collection.update_one(
            {
                "_id": validate_object_id(user_id),
                "tenant_id": tenant_id,
                "is_deleted": False,
            },
            {"$set": update_data},
        )

        return await self.get_by_id(user_id, tenant_id)

    async def soft_delete(self, user_id: str, tenant_id: str) -> bool:
        result = await self.collection.update_one(
            {
                "_id": validate_object_id(user_id),
                "tenant_id": tenant_id,
            },
            {
                "$set": {
                    "is_deleted": True,
                    "status": "DELETED",
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        return result.modified_count > 0

    async def store_refresh_token(self, token_data: dict) -> None:
        token_data["created_at"] = datetime.now(timezone.utc)
        await self.refresh_tokens.insert_one(token_data)

    async def revoke_refresh_token(self, token_hash: str) -> bool:
        result = await self.refresh_tokens.update_one(
            {"token_hash": token_hash},
            {
                "$set": {
                    "revoked": True,
                    "revoked_at": datetime.now(timezone.utc),
                }
            },
        )
        return result.modified_count > 0

    async def find_refresh_token(self, token_hash: str) -> dict | None:
        return await self.refresh_tokens.find_one(
            {
                "token_hash": token_hash,
                "revoked": False,
            }
        )