import requests, os, json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import insert
from backend.models import (
    Base, Restaurant, Location, Category, RestaurantCategory, OperatingHours, User, Review
)
from backend.utils.env import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, YELP_API_KEY

FOOD_CATEGORY_ROOTS = { "restaurants", "food", "cafe", "cafes", "coffee", "desserts", "bakeries", 
                       "bars", "pubs", "diners", "pizza", "ethnicfood", "seafood", "mideastern", 
                       "kosher", "breakfast_brunch", "sandwiches", "delis", "burgers"}
DIETARY_NEEDS = {"Vegan", "Vegetarian", "Halal", "Gluten-Free", "Kosher"}
FOOD_ALIAS_ROOTS = {"srilankan", "chinese"}

class YelpService:
    def __init__(self):
        self.api_key = YELP_API_KEY or os.getenv("YELP_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.base_url = "https://api.yelp.com/v3"

    def get_sqlalchemy_session(self):
        engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine)
        return SessionLocal()
        
    def fetch_all_categories(self):
        url = f"{self.base_url}/categories"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["categories"]
        
    def sync_yelp_categories(self):
        url = f"{self.base_url}/categories"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        categories = response.json().get("categories", [])

        session = self.get_sqlalchemy_session()
        added = 0

        for cat in categories:
            alias = cat.get("alias")
            title = cat.get("title")
            parents = ",".join(cat.get("parent_aliases", []))

            # Only insert if not already there
            existing = session.query(Category).filter_by(alias=alias).first()
            if not existing:
                new_cat = Category(
                    alias=alias,
                    name=title,
                    parent=parents
                )
                session.add(new_cat)
                added += 1

        session.commit()
        print(f"{added} new categories added to the DB.")

    def is_food_business(self, business: dict) -> bool:
        for category in business.get("categories", []):
            alias = category.get("alias", "").lower()

            if alias in FOOD_CATEGORY_ROOTS: # Match directly allowed categories
                return True
            
            if alias in FOOD_ALIAS_ROOTS:
                return True
            
            if any(alias.startswith(prefix) for prefix in FOOD_CATEGORY_ROOTS): # Match prefixes like "foodtrucks", "restaurantdelivery", etc.
                return True
            
            if any(alias.startswith(prefix) for prefix in FOOD_ALIAS_ROOTS): # Match prefixes like "srilankan"
                return True
        
        return False

    def fetch_businesses(self, term, location, limit=50, max_results=200):
        all_businesses = []
        for offset in range(0, max_results, limit):
            params = {
                "term": term,
                "location": location,
                "limit": limit,
                "offset": offset,
            }
            res = requests.get(f"{self.base_url}/businesses/search", headers=self.headers, params=params)
            if res.status_code != 200:
                print(f"Failed to fetch at offset {offset}: {res.status_code}")
                break
            batch = res.json().get("businesses", [])
            if not batch:
                break
            all_businesses.extend(batch)
        return all_businesses

    def store_yelp_data(self, businesses, term):
        print(f"store_yelp_data called with {len(businesses)} businesses")

        session = self.get_sqlalchemy_session()

        for biz in businesses:
            #if not self.is_food_business(biz):
            #    continue  # Skip non-food venues like museums

            loc = biz["location"]

            # ➤ Location insert
            location_stmt = insert(Location).values(
                address1=loc.get("address1"),
                address2=loc.get("address2"),
                address3=loc.get("address3"),
                city=loc.get("city"),
                zip_code=loc.get("zip_code"),
                country=loc.get("country"),
                state=loc.get("state"),
                display_address=", ".join(loc.get("display_address", [])),
            ).on_conflict_do_nothing()
            session.execute(location_stmt)

            location = session.query(Location).filter_by(
                address1=loc.get("address1"), city=loc.get("city")
            ).first()

            # ➤ Restaurant insert
            restaurant_insert_stmt = insert(Restaurant).values(
                yelp_id=biz["id"],
                name=biz["name"],
                alias=biz.get("alias"),
                image_url=biz.get("image_url"),
                is_closed=biz.get("is_closed", False),
                url=biz.get("url"),
                review_count=biz.get("review_count"),
                rating=biz.get("rating"),
                price=biz.get("price"),
                phone=biz.get("phone"),
                display_phone=biz.get("display_phone"),
                latitude=biz["coordinates"].get("latitude"),
                longitude=biz["coordinates"].get("longitude"),
                distance=biz.get("distance"),
                location_id=location.location_id if location else None,
                attributes=biz.get("attributes", {})
            )

            restaurant_stmt = restaurant_insert_stmt.on_conflict_do_update(
            index_elements=["yelp_id"],
            set_={
                "name": restaurant_insert_stmt.excluded.name,
                "review_count": restaurant_insert_stmt.excluded.review_count,
                "rating": restaurant_insert_stmt.excluded.rating,
                "price": restaurant_insert_stmt.excluded.price,
                "phone": restaurant_insert_stmt.excluded.phone,
                "latitude": restaurant_insert_stmt.excluded.latitude,
                "longitude": restaurant_insert_stmt.excluded.longitude,
                "is_closed": restaurant_insert_stmt.excluded.is_closed,
                "image_url": restaurant_insert_stmt.excluded.image_url,
                "url": restaurant_insert_stmt.excluded.url
                }
            )

            session.execute(restaurant_stmt)

            # ➤ Get saved restaurant object
            restaurant = session.query(Restaurant).filter_by(yelp_id=biz["id"]).first()

            # ➤ Insert Categories + Mapping
            # # Link Yelp categories
            # yelp_cats = [category["title"] for category in biz.get("categories", [])]
            # for cat_name in yelp_cats:
            #     category = session.query(Category).filter_by(name=cat_name).first()
            #     if not category:
            #         category = Category(name=cat_name, type="yelp")
            #         session.add(category)
            #         session.commit()
            #         session.refresh(category)

            #     # Link restaurant-category if not linked
            #     link = session.query(RestaurantCategory).filter_by(
            #                 restaurant_id=restaurant.restaurant_id,
            #                 category_id=category.category_id).first()
            #     if not link:
            #         link = RestaurantCategory(
            #             restaurant_id=restaurant.restaurant_id,
            #             category_id=category.category_id)
            #         session.add(link)
            #         session.commit()

            # # --- Inferred tag: if term not in Yelp categories, add term as custom category ---
            # if term not in yelp_cats:
            #     inferred_cat = session.query(Category).filter_by(name=term).first()
            #     if not inferred_cat:
            #         inferred_cat = Category(name=term, type="inferred")
            #         session.add(inferred_cat)
            #         session.commit()
            #         session.refresh(inferred_cat)

            #     # Link inferred category if not linked
            #     inferred_link = session.query(RestaurantCategory).filter_by(
            #         restaurant_id=restaurant.restaurant_id,
            #         category_id=inferred_cat.category_id
            #     ).first()
            #     if not inferred_link:
            #         inferred_link = RestaurantCategory(
            #             restaurant_id=restaurant.restaurant_id,
            #             category_id=inferred_cat.category_id
            #         )
            #         session.add(inferred_link)
            #         session.commit()

            for category in biz.get("categories", []):                
                db_category = session.query(Category).filter_by(alias=category["alias"]).first()
                if db_category:
                    session.execute(insert(RestaurantCategory).values(
                            restaurant_id=restaurant.restaurant_id,
                            category_id=db_category.category_id
                        ).on_conflict_do_nothing()
                    )
                    #session.add(rest_cat)

            # for cat in biz.get("categories", []):
            #     session.execute(insert(Category).values(name=cat["title"]).on_conflict_do_nothing())
            #     category = session.query(Category).filter_by(name=cat["title"]).first()
            #     if restaurant and category:
            #         session.execute(insert(RestaurantCategory).values(
            #             restaurant_id=restaurant.restaurant_id,
            #             category_id=category.category_id
            #         ).on_conflict_do_nothing())

            # ➤ Insert Operating Hours
            for bh in biz.get("business_hours", []):
                for open_time in bh.get("open", []):
                    session.execute(insert(OperatingHours).values(
                        location_id=location.location_id if location else None,
                        day_of_week=open_time["day"],
                        open_time=open_time["start"],
                        close_time=open_time["end"],
                        is_overnight=open_time["is_overnight"],
                        restaurant_id=restaurant.restaurant_id
                    ).on_conflict_do_nothing())

        session.commit()
        session.close()

    def load_and_store_yelp_data(self, location=str, term=str):
        businesses = self.fetch_businesses(term=term, location=location)
        print(f"Fetched {len(businesses)} businesses from Yelp")
        self.store_yelp_data(businesses, term)

        # Prepare path
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f"yelp_{term}.json")

        # Load existing businesses if file exists
        all_businesses = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                all_businesses = existing_data.get("businesses", [])

        # Add new businesses without duplicating by Yelp ID
        existing_ids = {biz["id"] for biz in all_businesses}
        new_unique_businesses = [biz for biz in businesses if biz["id"] not in existing_ids]
        all_businesses.extend(new_unique_businesses)

        # Save merged data
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"businesses": all_businesses}, f, indent=2)

        print(f"Merged data saved to {file_path} with {len(all_businesses)} total businesses.")

    # def fetch_and_save_reviews_for_restaurant(self, yelp_id: str, restaurant_id: int, session: Session):
    #     url = f"https://api.yelp.com/v3/businesses/{yelp_id}/reviews"
    #     response = requests.get(url, headers=self.headers)

    #     if response.status_code == 404:
    #         print(f"Reviews not found for {yelp_id}, skipping.")
    #         return
    #     elif response.status_code != 200:
    #         print(f"Failed to get reviews for {yelp_id}: {response.text}")
    #         return

    #     data = response.json()
    #     reviews = data.get("reviews", [])

    #     for r in reviews:
    #         user_data = r.get("user", {})
    #         username = user_data.get("name", "anonymous")
    #         # For demo, use username as unique email placeholder
    #         email = f"{username.replace(' ', '').lower()}@example.com"
    #         # You should hash a default password or generate random hash here
    #         hashed_password = "hashed_dummy_password"  # TODO: implement real hashing if needed

    #         # Check if user exists
    #         user = session.query(User).filter_by(email=email).first()
    #         if not user:
    #             user = User(
    #                 username=username,
    #                 email=email,
    #                 hashed_password=hashed_password,
    #                 role="user"
    #             )
    #             session.add(user)
    #             session.flush()  # To get user_id for FK

    #         review = Review(
    #             user_id=user.user_id,
    #             restaurant_id=restaurant_id,
    #             food_id=None,  # or link to a food if you want
    #             rating=r.get("rating", 0),
    #             comment=r.get("text", ""),
    #             created_at=datetime.strptime(r.get("time_created"), "%Y-%m-%d %H:%M:%S") if r.get("time_created") else datetime.utcnow()
    #         )
    #         session.add(review)

    #     session.commit()

    # def fetch_and_save_all_reviews(self):
    #     session = self.get_sqlalchemy_session()
    #     restaurants = session.query(Restaurant).filter(Restaurant.yelp_id != None).all()
    #     for restaurant in restaurants:
    #         print(f"Fetching reviews for {restaurant.name}")
    #         self.fetch_and_save_reviews_for_restaurant(restaurant.yelp_id, restaurant.restaurant_id, session)
    #     session.close()