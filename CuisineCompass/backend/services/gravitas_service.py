from sqlalchemy import or_
from backend.models import Restaurant, Location, Category
from backend.database.database import get_session
from backend.services.llm_service import LLMFactory
from sqlalchemy.orm import Session
from geopy.distance import geodesic

class GravitasService:
    def __init__(self):
        self.llm = LLMFactory.get_llm("together")

    def generate_route(self, location: str, cultures: str, db: Session) -> list[dict]:
        print(f"generate_route called with location={location}, cultures={cultures}")
        #session = get_session()
        #restaurants = self._get_cultural_restaurants(session, location, cultures)

        restaurants = self._get_cultural_restaurants(db, location, cultures)
        print(f"Found {len(restaurants)} restaurants from DB")
        if not restaurants:
            print("No restaurants matched filters.")
            return []

        top_restaurants = self._pick_best_per_culture(restaurants, cultures)
        print(f"Selected {len(top_restaurants)} top restaurants for route")

        route_prompt = self._build_prompt(top_restaurants, location, cultures)
        print("Prompt to LLM:\n", route_prompt)

        llm_response = self.llm.generate(route_prompt)
        print("LLM RAW RESPONSE:\n", llm_response)
        
        route = self._parse_route_response(llm_response)
        return route

    def _get_cultural_restaurants(self, db: Session, location: str, cultures: str):
        query = db.query(Restaurant).join(Restaurant.location).join(Restaurant.categories).join(Category)

        if location:
            query = query.filter(Location.city.ilike(f"%{location}%"))
        if cultures:
            filters = [Category.name.ilike(f"%{c.strip()}%") for c in cultures.split(",")]
            query = query.filter(or_(*filters))  # Use OR logic

        return query.limit(20).all()

    def _pick_best_per_culture(self, restaurants, cultures):
        selected = []
        used = set()

        for culture in cultures.split(","):
            for r in restaurants:
                for rc in r.categories:
                    if rc.category.name.lower() == culture.strip().lower() and r.restaurant_id not in used:
                        selected.append(r)
                        used.add(r.restaurant_id)
                        break
        return selected

    def _build_prompt(self, restaurants, location, cultures):
        entries = [f"{r.name}, located in {r.location.city}, serves {', '.join(c.category.name for c in r.categories)} cuisine."
                   for r in restaurants]

        joined = "\n".join(entries)

        return (
            f"The user wants to explore {cultures} cuisine around {location}. "
            f"Given the following restaurants:\n\n{joined}\n\n"
            f"Plan a food route that visits 3–5 of them in logical order. "
            f"For each stop, return dish name, restaurant name, address (with Street and city), culture, and one-line cultural description about the dish "
            f"Format output as:\n"
            f"1. Dish – Restaurant Name – Address – Culture – Cultural Description"
        )

    def _parse_route_response(self, raw: str):
        lines = [line.strip("0123456789. ").strip() for line in raw.strip().split("\n") if line.strip()]
        route = []

        for line in lines:
            parts = [p.strip() for p in line.split("–")]
            if len(parts) >= 5:
                route.append({
                    "dish": parts[0],
                    "restaurant_name": parts[1],
                    "address": parts[2],
                    "culture": parts[3],
                    "description": parts[4]
                })
        return route