from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    income = Column(Float, nullable=True)
    marital_status = Column(String, nullable=True)
    has_children = Column(Boolean, nullable=True)
    has_vehicle = Column(Boolean, nullable=True)
    has_home = Column(Boolean, nullable=True)
    has_medical_conditions = Column(Boolean, nullable=True)
    travel_frequency = Column(String, nullable=True)


# Pydantic Models
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    marital_status: Optional[str] = None
    has_children: Optional[bool] = None
    has_vehicle: Optional[bool] = None
    has_home: Optional[bool] = None
    has_medical_conditions: Optional[bool] = None
    travel_frequency: Optional[str] = None


class UserCredentialsRequest(UserBase):
    id: int
    name: str
    email: str
    is_verified: bool
    created_at: datetime


class UserResponse(UserBase):
    id: int
    name: str
    email: str
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse