from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.pipeline_orchestrator import run_pipeline

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "role": user.role,
        }
        for user in users
    ]


@router.get("/candidate-set/{user_id}")
def candidate_set(
    user_id: str,
    db: Session = Depends(get_db),
):
    return run_pipeline(db, user_id)