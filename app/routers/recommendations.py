from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import execute_sql_file
from app.models.recommendation_models import PreferenceCreate, PreferenceResponse, RecommendationWithInsurance
from app.services.recommendation_service import generate_recommendations
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.post("/preferences", response_model=PreferenceResponse)
def create_or_update_preferences(preferences: PreferenceCreate, current_user: dict = Depends(get_current_user)):
    # Check if user already has preferences
    existing_preferences = execute_sql_file(
        "recommendations/get_preferences_by_user.sql",
        {"user_id": current_user["id"]}
    )

    if existing_preferences:
        # Update existing preferences
        execute_sql_file("recommendations/update_preferences.sql", {
            "user_id": current_user["id"],
            "age": preferences.age,
            "income": preferences.income,
            "occupation": preferences.occupation,
            "health_condition": preferences.health_condition,
            "family_size": preferences.family_size
        })
    else:
        # Create new preferences
        execute_sql_file("recommendations/create_preferences.sql", {
            "user_id": current_user["id"],
            "age": preferences.age,
            "income": preferences.income,
            "occupation": preferences.occupation,
            "health_condition": preferences.health_condition,
            "family_size": preferences.family_size
        })

    # Generate recommendations based on preferences
    generate_recommendations(current_user["id"])

    # Get updated preferences
    updated_preferences = execute_sql_file(
        "recommendations/get_preferences_by_user.sql",
        {"user_id": current_user["id"]}
    )[0]

    return {
        "id": updated_preferences["id"],
        "user_id": updated_preferences["user_id"],
        "age": updated_preferences["age"],
        "income": updated_preferences["income"],
        "occupation": updated_preferences["occupation"],
        "health_condition": updated_preferences["health_condition"],
        "family_size": updated_preferences["family_size"],
        "created_at": updated_preferences["created_at"]
    }


@router.get("/", response_model=List[RecommendationWithInsurance])
def get_recommendations(current_user: dict = Depends(get_current_user)):
    recommendations = execute_sql_file(
        "recommendations/get_recommendations_by_user.sql",
        {"user_id": current_user["id"]}
    )

    return recommendations


@router.put("/{recommendation_id}/view")
def mark_recommendation_as_viewed(recommendation_id: int, current_user: dict = Depends(get_current_user)):
    # Check if recommendation exists and belongs to user
    recommendation = execute_sql_file(
        "recommendations/get_recommendation_by_id.sql",
        {"id": recommendation_id}
    )

    if not recommendation or recommendation[0]["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with ID {recommendation_id} not found"
        )

    # Mark as viewed
    execute_sql_file(
        "recommendations/mark_recommendation_viewed.sql",
        {"id": recommendation_id}
    )

    return {"message": "Recommendation marked as viewed"}


@router.put("/{recommendation_id}/purchase")
def mark_recommendation_as_purchased(recommendation_id: int, current_user: dict = Depends(get_current_user)):
    # Check if recommendation exists and belongs to user
    recommendation = execute_sql_file(
        "recommendations/get_recommendation_by_id.sql",
        {"id": recommendation_id}
    )

    if not recommendation or recommendation[0]["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with ID {recommendation_id} not found"
        )

    # Mark as purchased
    execute_sql_file(
        "recommendations/mark_recommendation_purchased.sql",
        {"id": recommendation_id}
    )

    return {"message": "Recommendation marked as purchased"}
