from pydantic import BaseModel


class Permission(BaseModel):
    can_read: bool
    can_write: bool


class PermissionContext(BaseModel):
    user_id: str
    role: str
    department: str
    org_id: str
    ceiling_level: int
    write_ceiling: int | None = None
    compliance_clearance: list[str]

    permissions: dict[int, Permission]