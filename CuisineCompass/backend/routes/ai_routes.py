from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas import *
from backend.auth.auth import get_current_user
from backend.models import User
from backend.database.database import get_session
from backend.services.recommendation_service import RecommendationService
from backend.services.chat_service import ChatService
from backend.services.similarity_service import SimilarityService
from backend.services.moderation_service import ModerationService
from backend.services.gravitas_service import GravitasService

router = APIRouter()
rec_service = RecommendationService()
chat_service = ChatService()
sim_service = SimilarityService()
mod_service = ModerationService()
gravitas_service = GravitasService()

@router.get("/recommendations/personalized", response_model=List[RecommendationOut], summary="Get personalized restaurant recommendations")
def get_personalized(db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return rec_service.get_personalized_recommendations(user, db)

@router.get("/recommendations/similar", response_model=List[RecommendationOut], summary="Find similar restaurants by theme but different cuisine")
def similar(source_restaurant: str, target_cuisine: str):
    return sim_service.find_similar_with_twist(source_restaurant, target_cuisine)

@router.post("/chat", response_model=ChatResponse, summary="Chat with cultural concierge")
def chat(input: ChatInput):
    reply = chat_service.respond(input.question, input.location, input.time)
    return {"response": reply}

@router.post("/moderate/review", response_model=ModerationResult, summary="Moderate a review")
def moderate(comment: str):
    return mod_service.moderate_review(comment)

@router.get("/gravitas/route", response_model=List[GravitasStop], summary="Get a cultural food journey route")
def get_food_route(location: str, cultures: str):
    return gravitas_service.generate_route(location, cultures)
