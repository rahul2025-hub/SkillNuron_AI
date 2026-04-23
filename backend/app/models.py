"""SQLAlchemy models for database tables."""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    JOBSEEKER = "jobseeker"
    RECRUITER = "recruiter"


class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.JOBSEEKER)

    skills = relationship("Skill", back_populates="owner")


class Skill(Base):
    """Skill model for user skill profiles."""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level = Column(Integer)  # 0-100
    category = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="skills")


class Job(Base):
    """Job posting model."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    type = Column(String)
    salary_range = Column(String)
    description = Column(Text)
    required_skills = Column(String)  # Stored as comma-separated string for simplicity
    posted_date = Column(String)