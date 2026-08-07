from sqlalchemy.orm import Session

from app.models.user import User
from app.models.hierarchy_level import HierarchyLevel
from fastapi import HTTPException


class EntryPointResolver:
    def resolve(self, db: Session, user_id: str):
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ValueError("User not found.")
            

        if user.role == "ADMIN":
            root = (
                db.query(HierarchyLevel)
                .filter(HierarchyLevel.level_number == 1)
                .first()
            )
            if root is None:
                raise ValueError("Root hierarchy node not found.")
            return root.id

        dept_levels = (
            db.query(HierarchyLevel)
            .filter(HierarchyLevel.department == user.department)
            .all()
        )
        if not dept_levels:
            raise HTTPException(
            status_code=404,
            detail=f"No hierarchy configured for department {user.department}"
    )

        if not dept_levels:
            raise ValueError(f"No hierarchy found for department {user.department}")

        if user.role == "HOD":
            # HOD enters at their department's own anchor —
            # the shallowest (lowest level_number) row in their dept
            entry = min(dept_levels, key=lambda h: h.level_number)
        else:
            # VIEWER / EDITOR / QUALITY / AUDITOR enter at the
            # ward level specifically (level_number == 10), since
            # that's the most operational/specific node, not the
            # absolute deepest (which would incorrectly land on
            # patient-level nodes like level 12)
            ward_level = next(
                (h for h in dept_levels if h.level_number == 10), None
            )
            entry = ward_level if ward_level is not None else max(
                dept_levels, key=lambda h: h.level_number
            )

        return entry.id