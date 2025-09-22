from backend.models import Review, Favorite, Restaurant
from backend.services.llm_service import LLMFactory

class RecommendationService:
    def __init__(self):
        self.llm = LLMFactory.get_llm("together")

    def get_user_cuisine_preferences(self, user, db):
        favorites = db.query(Favorite).filter_by(user_id=user.user_id).all()
        cuisines = []
        for fav in favorites:
            restaurant = db.query(Restaurant).filter_by(restaurant_id=fav.restaurant_id).first()
            if restaurant:
                for cat in restaurant.categories:
                    cuisines.append(cat.category.name)
        return list(set(cuisines))

    def get_personalized_recommendations(self, user, db):
        cuisines = self.get_user_cuisine_preferences(user, db)
        past_reviews = db.query(Review).filter_by(user_id=user.user_id).all()
        review_summary = "\n".join([f"{db.query(Restaurant).get(r.restaurant_id).name} (rated {r.rating})" for r in past_reviews])
        prompt = (
            f"You are a multicultural food guide. The user enjoys {', '.join(cuisines)} cuisine and has liked:\n"
            f"{review_summary}\nSuggest 3 multicultural restaurants nearby in Auckland. Include one-line cultural context."
        )
        response = self.llm.generate(prompt)
        return self._parse(response)

    def _parse(self, raw):
        lines = raw.split("\n")
        output = []
        for line in lines:
            if not line.strip(): continue
            parts = line.split("–")
            if len(parts) >= 2:
                output.append({
                    "name": parts[0].strip(),
                    "cultural_context": parts[1].strip()
                })
        return output
