# backend/services/food_service.py

from backend.database.database import get_session
from backend.models import Food, Category, Restaurant, Location
#from backend.services.llm_service import HuggingFaceProvider  # or your LLM service
from sqlalchemy.orm import Session

class FoodService:
    def __init__(self):
        self.llm = None #HuggingFaceProvider()

    def generate_foods_for_restaurant(self, restaurant: Restaurant, session: Session):
        # Get category titles of this restaurant
        categories = []
        for rc in restaurant.categories:
            if hasattr(rc, "category") and rc.category and hasattr(rc.category, "name"):
                categories.append(rc.category.name)
        
        if not categories:
            categories = ["general"]

        # Compose prompt for LLM
        prompt = (
            f"List 5 popular dishes served at a restaurant with these categories: {', '.join(categories)}. "
            "For each dish, provide only the name."
        )

        # Get LLM response
        response = self.llm.generate(prompt)  # Adjust if async or different API
        
        # Parse response (assuming comma or newline separated)
        dish_names = []
        if response:
            # Try splitting on newlines or commas
            if "\n" in response:
                dish_names = [line.strip("- ").strip() for line in response.split("\n") if line.strip()]
            else:
                dish_names = [dish.strip() for dish in response.split(",") if dish.strip()]
        else:
            dish_names = []

        category_objs = session.query(Category).filter(Category.name.in_(categories)).all()
        category_map = {c.name: c for c in category_objs}

        # Choose one category ID to assign (e.g., first one)
        category_id = category_objs[0].category_id if category_objs else None

        # Save to DB, avoid duplicates
        for dish_name in dish_names:
            existing = session.query(Food).filter(
                Food.restaurant_id == restaurant.restaurant_id,
                Food.name.ilike(dish_name)
            ).first()
            if existing:
                continue

            # Optionally find category_id matching any category name
            #category_obj = session.query(Category).filter(Category.name.in_(categories)).first()

            new_food = Food(
                restaurant_id=restaurant.restaurant_id,
                name=dish_name,
                description=None,
                price=None,
                category_id=category_id
            )
            session.add(new_food)

        session.commit()

    def generate_foods_for_location(self, location: str):
        session = get_session()
        restaurants = session.query(Restaurant).join(Restaurant.location).filter(
            Location.city.ilike(f"%{location}%")
        ).all()
        for restaurant in restaurants:
            self.generate_foods_for_restaurant(restaurant, session)
        session.close()
