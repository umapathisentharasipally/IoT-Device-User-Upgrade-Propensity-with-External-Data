from pydantic import BaseModel


class PermissionDTO(BaseModel):
    permission_name: str
    module: str
    action: str
    description: str | None = None