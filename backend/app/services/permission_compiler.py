from sqlalchemy.orm import Session

from app.models.user import User
from app.models.hierarchy_level import HierarchyLevel


class PermissionCompiler:

    def compile(self, db: Session, user_id: str) -> dict:

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ValueError(f"User '{user_id}' not found.")

        # ONE query — fetch all hierarchy levels once
        hierarchy_levels = db.query(HierarchyLevel).all()

        permission_lookup = {}

        full_read = user.role in ("HOD", "ADMIN")
        full_write = user.role == "ADMIN"

        # Dedupe level numbers first — several hierarchy_levels rows
        # share the same level_number across departments, so there's
        # no need to recompute the same permission value repeatedly
        distinct_levels = {h.level_number for h in hierarchy_levels}

        for level in distinct_levels:
            can_read = full_read or level >= user.ceiling_level
            can_write = full_write or (
                user.write_ceiling is not None and level >= user.write_ceiling
            )

            permission_lookup[level] = {
                "can_read": can_read,
                "can_write": can_write,
            }

        return permission_lookup