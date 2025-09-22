from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from backend.database.database import get_session
from backend.schemas import ReviewCreate, ReviewResponse, ModerationResult
from backend.models import Review, User, Restaurant
from backend.services.yelp_service import YelpService  # Ensure this import path is correct
from backend.services.moderation_service import ModerationService

router = APIRouter()
yelp_service = YelpService()  # Initialize your Yelp service
mod_service = ModerationService()

@router.post("/addReview/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_session)):
    # Submit a review. A user can only submit one review per restaurant per food item.
    # Prevent duplicate review for same user, restaurant, and food (optional)
    existing_review = db.query(Review).filter(
        Review.user_id == review.user_id,
        Review.restaurant_id == review.restaurant_id
        #Review.food_id == review.food_id
    ).first()

    if existing_review:
        raise HTTPException(status_code=400, detail="Duplicate review: user has already reviewed this restaurent.")

    # Sentiment analysis placeholder (to be implemented later)
    # sentiment = llm.analyze_sentiment(review.comment)

    # Create and save the review
    new_review = Review(
        user_id=review.user_id,
        restaurant_id=review.restaurant_id,
        #food_id=review.food_id,
        rating=review.rating,
        comment=review.comment,
        # sentiment=sentiment (once sentiment analysis is added and column exists)
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.delete("/deleteReview/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_session)):
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}

# @router.get("/")
# def get_all_reviews(session: Session = Depends(get_session)):
#     return session.query(Review).all()

@router.get("/by_restaurant/{restaurant_id}")
def get_reviews_by_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    #reviews = session.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    reviews = session.query(Review).join(Review.user).filter(Review.restaurant_id == restaurant_id).all()
    #return reviews
    return [
        {
            "id": rev.review_id,
            "user": { 
                "name": rev.user.username if rev.user else "Unknown User",
                "avatar": "",
                "location": "Auckland, NZ"
                },
            "rating": rev.rating,
            "date": rev.created_at,
            "content": rev.comment,
        } for rev in reviews
    ]

# Optional: get reviews by user
@router.get("/by_user/{user_id}")
def get_reviews_by_user(user_id: int, session: Session = Depends(get_session)):
    reviews = session.query(Review).filter(Review.user_id == user_id).all()
    return reviews

@router.get("/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_session)):
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/moderate", response_model=ModerationResult, summary="Moderate a review")
def moderate(comment: str):
    return mod_service.moderate_review(comment)
# @router.post("/all")
# def fetch_all_reviews():
#     yelp_service.fetch_and_save_all_reviews()
#     return {"message": "Started fetching all Yelp reviews."}