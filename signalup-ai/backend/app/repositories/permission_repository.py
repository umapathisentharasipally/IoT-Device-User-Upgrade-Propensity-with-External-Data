from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase


class PermissionRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.permissions

    async def seed_permissions(self, permissions: list[str]) -> None:
        for permission in permissions:
            existing = await self.collection.find_one({"permission_name": permission})
            if existing:
                continue

            module, action = permission.split(".", 1)

            await self.collection.insert_one(
                {
                    "permission_name": permission,
                    "module": module,
                    "action": action,
                    "description": f"{action} access for {module}",
                    "created_at": datetime.now(timezone.utc),
                }
            )

    async def list_permissions(self) -> list[dict]:
        cursor = self.collection.find({}).sort("permission_name", 1)
        return await cursor.to_list(length=500)