from typing import Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.database import get_database
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_token(token, expected_type="access")

    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")

    if not user_id or not tenant_id:
        raise UnauthorizedException("Invalid token payload.")

    db = get_database()
    user_repository = UserRepository(db)

    user = await user_repository.get_by_id(user_id=user_id, tenant_id=tenant_id)

    if not user:
        raise UnauthorizedException("User not found.")

    if user.get("status") != "ACTIVE":
        raise UnauthorizedException("User account is inactive.")

    user["_id"] = str(user["_id"])
    return user


def require_permissions(required_permissions: list[str]) -> Callable:
    async def permission_dependency(
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        user_permissions = set(current_user.get("permissions", []))

        if "admin.all" in user_permissions:
            return current_user

        missing_permissions = [
            permission
            for permission in required_permissions
            if permission not in user_permissions
        ]

        if missing_permissions:
            raise ForbiddenException("You do not have required permissions.")

        return current_user

    return permission_dependency