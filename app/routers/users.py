from fastapi import APIRouter, Depends
from app.database import execute_sql_file
from app.models.user_models import UserResponse, UserCredentialsRequest, UserUpdate
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/get_user_creds", response_model=UserResponse)
def get_current_user_info(request: UserCredentialsRequest, current_user: dict = Depends(get_current_user)):
    """Get user credentials"""
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "is_verified": current_user["is_verified"],
        "created_at": current_user["created_at"]
    }


@router.put("/update_info", response_model=UserResponse)
def update_user_info(user_data: UserUpdate, current_user: dict = Depends(get_current_user)):
    """Update user info"""
    sql_params = {**user_data.dict(exclude_unset=True), "id": current_user["id"]}

    execute_sql_file("users/update_user_info.sql", sql_params)

    updated_user = execute_sql_file("users/get_user_by_id.sql", {"id": current_user["id"]})[0]

    return {
        "id": updated_user["id"],
        "name": updated_user["name"],
        "email": updated_user["email"],
        "is_verified": updated_user["is_verified"],
        "created_at": updated_user["created_at"]
    }