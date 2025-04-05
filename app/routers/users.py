from fastapi import APIRouter, Depends, HTTPException, status
from app.database import execute_sql_file
from app.models.user_models import UserResponse
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "is_verified": current_user["is_verified"],
        "created_at": current_user["created_at"]
    }


@router.put("/me", response_model=UserResponse)
def update_user_info(user_data: dict, current_user: dict = Depends(get_current_user)):
    # Update user information
    execute_sql_file("users/update_user.sql", {
        "id": current_user["id"],
        "name": user_data.get("name", current_user["name"])
    })

    # Get updated user
    updated_user = execute_sql_file("users/get_user_by_id.sql", {"id": current_user["id"]})[0]

    return {
        "id": updated_user["id"],
        "name": updated_user["name"],
        "email": updated_user["email"],
        "is_verified": updated_user["is_verified"],
        "created_at": updated_user["created_at"]
    }