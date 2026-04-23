"""Skills management router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, deps

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/", response_model=List[schemas.SkillResponse])
def read_skills(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> List[schemas.SkillResponse]:
    """Get all skills for the current user."""
    return current_user.skills


@router.post("/", response_model=schemas.SkillResponse)
def create_skill(
    skill: schemas.SkillCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.SkillResponse:
    """Add a new skill to the user's profile."""
    db_skill = models.Skill(**skill.dict(), user_id=current_user.id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.delete("/{skill_name}")
def delete_skill(
    skill_name: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    """Delete a skill from the user's profile."""
    skill = db.query(models.Skill).filter(
        models.Skill.user_id == current_user.id,
        models.Skill.name == skill_name,
    ).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted"}