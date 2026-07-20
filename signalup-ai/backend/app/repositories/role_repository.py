from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.utils.object_id import validate_object_id


class RoleRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.roles

    async def create(self, role_data: dict) -> dict:
        role_data["created_at"] = datetime.now(timezone.utc)
        role_data["updated_at"] = datetime.now(timezone.utc)
        role_data["is_deleted"] = False

        result = await self.collection.insert_one(role_data)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get_by_id(self, role_id: str, tenant_id: str) -> dict | None:
        return await self.collection.find_one(
            {
                "_id": validate_object_id(role_id),
                "tenant_id": tenant_id,
                "is_deleted": False,
            }
        )

    async def get_by_name(self, role_name: str, tenant_id: str) -> dict | None:
        return await self.collection.find_one(
            {
                "tenant_id": tenant_id,
                "role_name": role_name,
                "is_deleted": False,
            }
        )

    async def list_roles(self, tenant_id: str) -> list[dict]:
        cursor = self.collection.find(
            {
                "tenant_id": tenant_id,
                "is_deleted": False,
            }
        ).sort("created_at", -1)
        return await cursor.to_list(length=100)

    async def update(self, role_id: str, tenant_id: str, update_data: dict) -> dict | None:
        update_data["updated_at"] = datetime.now(timezone.utc)

        await self.collection.update_one(
            {
                "_id": validate_object_id(role_id),
                "tenant_id": tenant_id,
                "is_deleted": False,
            },
            {"$set": update_data},
        )

        return await self.get_by_id(role_id, tenant_id)

    async def soft_delete(self, role_id: str, tenant_id: str) -> bool:
        result = await self.collection.update_one(
            {
                "_id": validate_object_id(role_id),
                "tenant_id": tenant_id,
            },
            {
                "$set": {
                    "is_deleted": True,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        return result.modified_count > 0