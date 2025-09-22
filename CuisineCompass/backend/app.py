from fastapi import FastAPI, Depends
from backend.database.database import DatabaseConnection
from backend.routes import gravitas, favourites, admin_routes
from backend.services.yelp_service import YelpService
from backend.auth.auth import get_current_user
from backend.models import User
from backend.routes import auth_routes, food_routes, llm_routes, restaurant_routes, review_routes, user_routes, ai_routes

app = FastAPI(title="Multicultural Cuisine Compass")
yelp = YelpService()

@app.get("/")
def root():
    return {"message": "Welcome to the Multicultural Cuisine Compass API!"}

@app.on_event("startup")
def on_startup():
    db = DatabaseConnection()
    print("Database connection initialized.")
    print("Connected to PostgreSQL.")
    #yelp.sync_yelp_categories()

# @app.get("/fetch/yelp")
# def fetch_yelp(term: str = "indian", location: str = "Auckland"):
#     yelp.load_and_store_yelp_data(term, location)
#     return {"status": f"Fetched Yelp data for '{term}' in '{location}'"}

# @app.get("/fetch/yelp/all")
# def fetch_all_yelp_restaurants(location: str = "Auckland"):
#     cuisines = ["Indian", "Japanese", "Thai", "Italian", "Mexican", "Chinese", "Greek", "French", "Turkish", "Vietnamese", "Sri Lankan", "Korean", "Spanish", "Malaysian", "Indonesian", "Filipino", "Pakistani", "Bangladeshi", "Middle Eastern"]
#     for cuisine in cuisines:
#         print(f"📦 Fetching {cuisine} restaurants in {location}...")
#         yelp.load_and_store_yelp_data(term=cuisine, location=location)
#     return {"status": f"Fetched data for multiple cuisines in {location}"}

# @app.get("/fetch/reviews/all")
# def fetch_all_reviews():
#     yelp.fetch_and_save_all_reviews()
#     return {"message": "Started fetching all Yelp reviews."}

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}

# Route registrations
app.include_router(auth_routes.auth_router)
app.include_router(admin_routes.router)
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(restaurant_routes.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(favourites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(food_routes.router, prefix="/foods", tags=["foods"])
app.include_router(review_routes.router, prefix="/reviews", tags=["reviews"])
app.include_router(llm_routes.router)
app.include_router(ai_routes.router, prefix="/ai", tags=["AI Features"])
app.include_router(gravitas.router, prefix="/gravitas", tags=["Gravitas Route"])

# # Start background job scheduler
# start_scheduler_for_culture_stories()
# start_scheduler_for_restaurent_summary()