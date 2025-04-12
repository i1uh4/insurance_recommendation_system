from fastapi import APIRouter, HTTPException, status
from app.database import execute_sql_file
from app.models.user_models import UserCreate, UserLogin, Token
from app.utils.auth import create_access_token, get_password_hash, verify_password
from app.services.email_service import send_verification_email
from app.services.auth_service import verify_token
import logging

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=dict)
async def register_user(user: UserCreate):
    """Register a new user"""
    existing_user = execute_sql_file("users/get_user_by_email.sql", {"email": user.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    hashed_password = get_password_hash(user.password)

    execute_sql_file("users/create_user.sql", {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    })

    created_user = execute_sql_file("users/get_user_by_email.sql", {"email": user.email})[0]

    try:
        await send_verification_email(user.email, created_user["id"])
        logging.info(f"Verification email sent to {user.email}")
    except Exception as e:
        logging.error(f"Failed to send verification email: {str(e)}")

    return {
        "code": 0,
        "message": "User registered successfully. Please check your email for verification."
    }


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin):
    """Login a user"""
    user_result = execute_sql_file("users/get_user_by_email.sql", {"email": user_credentials.email})

    if not user_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    user = user_result[0]

    if not verify_password(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user["id"], "email": user["email"]})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "is_verified": user["is_verified"],
            "created_at": user["created_at"]
        }
    }


@router.get("/verify/{token}")
def verify_email(token: str):
    """Verify a user's email"""
    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )

        execute_sql_file("users/verify_user.sql", {"id": user_id})

        return {"message": "Email verified successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid verification token: {str(e)}"
        )
