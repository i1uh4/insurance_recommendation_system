from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.insurance_models import InsuranceResponse


# SQLAlchemy Models
class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    age = Column(Integer)
    income = Column(Float)
    occupation = Column(String)
    health_condition = Column(String)
    family_size = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    insurance_id = Column(Integer, ForeignKey("insurances.id"))
    score = Column(Float)
    is_viewed = Column(Boolean, default=False)
    is_purchased = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Pydantic Models
class PreferenceBase(BaseModel):
    age: int
    income: float
    occupation: str
    health_condition: str
    family_size: int


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceResponse(PreferenceBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RecommendationBase(BaseModel):
    user_id: int
    insurance_id: int
    score: float
    is_viewed: Optional[bool] = False
    is_purchased: Optional[bool] = False


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationResponse(RecommendationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RecommendationWithInsurance(RecommendationResponse):
    insurance: InsuranceResponse

    class Config:
        orm_mode = True
