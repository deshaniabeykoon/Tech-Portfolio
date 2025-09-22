from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from fastapi import Form

class LoginRequest(BaseModel):
    user_email: EmailStr
    password: str

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str  # plaintext from user

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True  # allows SQLAlchemy model to be returned directly

class OAuth2EmailRequestForm:
    def __init__(
        self,
        user_email: str = Form(..., alias="username", description="User email"),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: str = Form(None),
        client_secret: str = Form(None),
    ):
        self.username = user_email  # Keep compatibility
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret

# Pydantic schema for review creation
class ReviewCreate(BaseModel):
    user_id: int
    restaurant_id: int
    #food_id: int | None = None
    rating: float
    comment: Optional[str]
    created_at: datetime | None = None

class ReviewResponse(BaseModel):
    review_id: int
    user_id: int
    restaurant_id: int
    #food_id: Optional[int]
    rating: float
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class CategorySchema(BaseModel):
    category_id: int
    name: str
    type: Optional[str]

    class Config:
        orm_mode = True

class RestaurantSchema(BaseModel):
    restaurant_id: int
    name: str
    location: Optional[str]
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    categories: Optional[List[CategorySchema]] = []

    class Config:
        orm_mode = True

class RestaurantCreate(BaseModel):
    yelp_id: Optional[str]
    name: str
    alias: Optional[str]
    image_url: Optional[str]
    is_closed: Optional[bool]
    url: Optional[str]
    review_count: Optional[int]
    rating: Optional[float]
    price: Optional[str]
    phone: Optional[str]
    display_phone: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    distance: Optional[float]
    transactions: Optional[List[str]]
    business_hours: Optional[Dict[str, Any]] = None
    attributes: Optional[Dict[str, Any]] = None
    location_id: Optional[int]

    class Config:
        orm_mode = True

class RestaurantResponse(RestaurantCreate):
    restaurant_id: int

class RestaurantUpdate(BaseModel):
    yelp_id: Optional[str]
    name: Optional[str]
    alias: Optional[str]
    image_url: Optional[str]
    is_closed: Optional[bool]
    url: Optional[str]
    review_count: Optional[int]
    rating: Optional[float]
    price: Optional[str]
    phone: Optional[str]
    display_phone: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    transactions: Optional[List[str]]
    business_hours: Optional[Dict]
    attributes: Optional[Dict]
    location_id: Optional[int]

    class Config:
        orm_mode = True

# backend/schemas.py

class RestaurantResponse(BaseModel):
    restaurant_id: int
    name: str
    alias: Optional[str]
    yelp_id: Optional[str]
    is_closed: Optional[bool]
    image_url: Optional[str]
    url: Optional[str]
    review_count: Optional[int]
    rating: Optional[float]
    price: Optional[str]
    phone: Optional[str]
    display_phone: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    location_id: Optional[int]  # Assuming location is a ForeignKey

    class Config:
        orm_mode = True

class RestaurantStoryResponse(BaseModel):
    about_id: int
    restaurant_id: int
    summary: str
    last_updated: datetime

    class Config:
        orm_mode = True

class FavoriteCreate(BaseModel):
    restaurant_id: int

class FavoriteRestaurantOut(BaseModel):
    restaurant_id: int
    restaurant_name: str

    class Config:
        orm_mode = True

class CultureStoryCreate(BaseModel):
    food_name: str
    image_url: Optional[str]
    origin_country: Optional[str] = None

class CultureStoryResponse(BaseModel):
    story_id: int
    food_id: int
    food_name: str
    image_url: Optional[str]
    origin_country: Optional[str]
    story_summary: Optional[str]
    story: Optional[str]

    class Config:
        orm_mode = True

class FoodFactRequest(BaseModel):
    food_name: str = Field(..., example="Konda Kavum")
    provider: Literal["openai", "deepseek", "llama", "huggingface", "together"] = Field(default="together", example="deepseek")

class FoodFactResponse(BaseModel):
    food_name: str
    provider: str
    summary: str
    fact: str

class AboutPageRequest(BaseModel):
    restaurant_name: str
    provider: Literal["openai", "deepseek", "llama", "huggingface", "together"] = "together"

class RestaurantSummary(BaseModel):
    restaurant_id: int
    name: str
    summary: str | None  # summary can be nullable

class RecommendationOut(BaseModel):
    name: str
    location: Optional[str]
    cuisine: Optional[str]
    cultural_context: str

class TravelRecOut(BaseModel):
    dish: str
    restaurant: str
    culture: str
    reason: str

class ChatInput(BaseModel):
    question: str
    location: Optional[str] = "Auckland"
    time: Optional[str] = datetime.utcnow().isoformat()

class ChatResponse(BaseModel):
    response: str

class SimilarityInput(BaseModel):
    source_restaurant: str
    target_cuisine: str

class ModerationResult(BaseModel):
    is_safe: bool
    toxicity_level: str
    sentiment: str
    flags: List[str]

class GravitasStop(BaseModel):
    dish: str
    restaurant_name: str
    address: str
    culture: str
    description: str

class RestaurantBrowseQuery(BaseModel):
    location: str = Field(..., example="Auckland")
    cuisine: Optional[str] = Field(None, example="Chinese")
    scene: Optional[str] = Field(None, example="Restaurant")
    special_diet: Optional[str] = Field(None, example="Vegan")
    name: Optional[str] = Field(None, example="Depot")
    match_any: Optional[bool] = Field(True, description="Match any category instead of all")