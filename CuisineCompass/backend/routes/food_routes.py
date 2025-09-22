from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from backend.routes.llm_routes import *
from backend.services.food_service import FoodService
from backend.database.database import DatabaseConnection, get_session
from backend.models import Food, CultureStory
from backend.schemas import CultureStoryResponse, CultureStoryCreate  # Add this import or adjust the path as needed
from backend.scheduler import generate_and_store_food_stories
from typing import List

router = APIRouter()
food_service = FoodService()

# @router.get("/")
# def list_all_foods(db: Session = Depends(get_session)):
#     return db.query(Food).all()

@router.get("/")
def list_all_foods():
    db = DatabaseConnection()  # Create instance
    session: Session = db.get_session()  # Call instance method
    return session.query(Food).all()

@router.get("/by_restaurant/{restaurant_id}")
def list_foods_by_restaurant(restaurant_id: int):
    db = DatabaseConnection()
    session: Session = db.get_session()
    return session.query(Food).filter(Food.restaurant_id == restaurant_id).all()

# @router.post("/generate")
# async def generate_foods_post(location: str = Query(..., description="City or area name to generate foods for")):
#     try:
#         food_service.generate_foods_for_location(location)
#         return {"message": f"Food generation started for restaurants in {location}"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/generate")
# async def generate_foods_get(location: str = Query(..., description="City or area name to generate foods for")):
#     try:
#         food_service.generate_foods_for_location(location)
#         return {"message": f"Food generation started for restaurants in {location}"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/cultural-stories", response_model=List[CultureStoryResponse])
def get_food_stories(db: Session = Depends(get_session)):
    return db.query(CultureStory).filter(
        and_(
            CultureStory.story.isnot(None),
            CultureStory.story != ""
        )
    ).all()

@router.post("/cultural-stories/add", response_model=CultureStoryResponse)
def add_culture_story(
    input_data: CultureStoryCreate,
    db: Session = Depends(get_session)
):
    if not input_data.food_name:
        raise HTTPException(status_code=400, detail="Food name is required")

    # Optional: check if already exists
    existing = db.query(CultureStory).filter(
        CultureStory.food_name == input_data.food_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="This food already exists in stories.")

    new_entry = CultureStory(
        food_name=input_data.food_name,
        image_url = input_data.image_url,
        origin_country=input_data.origin_country
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

@router.post("/generate-food-stories", response_model=dict)
def generate_and_save_food_stories():
    """
    Generate and update cultural food stories where story is missing.
    """
    generate_and_store_food_stories()
    return {"message": "Cultural stories generated (if any missing) and updated in DB."}