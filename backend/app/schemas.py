"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

from .models import UserRole


# --- Auth Schemas ---
class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str
    role: UserRole


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str
    user_id: int
    user_name: str
    role: str


# --- Skill Schemas ---
class SkillBase(BaseModel):
    """Base skill schema."""
    name: str
    level: int = Field(..., ge=0, le=100)
    category: str


class SkillCreate(SkillBase):
    """Schema for creating a skill."""
    pass


class SkillResponse(SkillBase):
    """Schema for skill response."""
    id: int
    user_id: int

    class Config:
        from_attributes = True


# --- Job Schemas ---
class JobResponse(BaseModel):
    """Schema for job response with match score."""
    id: int
    title: str
    company: str
    location: str
    type: str
    salary: str = Field(alias="salary_range")
    requiredSkills: List[str]
    description: str
    postedDate: str
    matchScore: Optional[int] = 0

    class Config:
        from_attributes = True