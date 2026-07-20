from typing import Optional

from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    tenant_id: str
    role_name: str = Field(..., min_length=2)
    description: Optional[str] = None
    permissions: list[str] = []


class RoleUpdate(BaseModel):
    role_name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[list[str]] = None


class RoleDTO(BaseModel):
    id: str
    tenant_id: str
    role_name: str
    description: Optional[str] = None
    permissions: list[str] = []