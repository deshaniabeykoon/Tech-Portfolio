from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.database import get_session
from backend.models import Favorite, Restaurant, User
from backend.auth.auth import get_current_user  # assuming JWT-based auth

from backend.schemas import FavoriteCreate, FavoriteRestaurantOut
from typing import List

router = APIRouter()

# Add Favourite
@router.post("/")
def add_favorite(
    favorite_data: FavoriteCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Only registered users can favorite restaurants.")

    # check if restaurant exists
    restaurant = db.query(Restaurant).filter_by(restaurant_id=favorite_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found.")

    # check if already favorited
    existing = db.query(Favorite).filter_by(user_id=current_user.user_id, restaurant_id=restaurant.restaurant_id).first()
    if existing:
        return {"message": "Restaurant already marked as favorite."}

    favorite = Favorite(user_id=current_user.user_id, restaurant_id=restaurant.restaurant_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return {"message": "Restaurant added to favorites."}

# Remove favourite
@router.delete("/{restaurant_id}", status_code=status.HTTP_200_OK)
def remove_favorite(
    restaurant_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Only registered users can remove favorites.")

    favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == current_user.user_id, Favorite.restaurant_id == restaurant_id)
        .first()
    )
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
    return {"message": f"Restaurant favorite removed."}




@router.get("/by_user", response_model=List[FavoriteRestaurantOut])
def get_user_favorites(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Only registered users have favorites.")

    favorites = (
        db.query(Favorite)
        .filter_by(user_id=current_user.user_id)
        .join(Restaurant, Favorite.restaurant_id == Restaurant.restaurant_id)
        .all()
    )

    return [
        FavoriteRestaurantOut(
            restaurant_id=fav.restaurant.restaurant_id,
            restaurant_name=fav.restaurant.name,
        )
        for fav in favorites
    ]

