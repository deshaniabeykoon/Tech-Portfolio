from sqlalchemy import Sequence, Column, Integer, String, Float, Boolean, JSON, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # e.g., user, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="user")
    photos = relationship("Photo", back_populates="user")

class Location(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    city = Column(String)
    zip_code = Column(String)
    country = Column(String)
    state = Column(String)
    display_address = Column(String)  # maybe JSON or concatenated string

    restaurants = relationship("Restaurant", back_populates="location")
    operating_hours = relationship("OperatingHours", back_populates="location")

    __table_args__ = (
    UniqueConstraint("address1", "city", "zip_code", name="uix_location_unique"),
)

class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(Integer, primary_key=True, index=True)
    restaurant_description = Column(String, nullable=True)  # Optional description
    yelp_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    alias = Column(String)
    image_url = Column(String)
    is_closed = Column(Boolean, default=False)
    url = Column(String)
    review_count = Column(Integer)
    rating = Column(Float)
    price = Column(String)
    phone = Column(String)
    display_phone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    distance = Column(Float)

    # Location info is linked in Location table

    # Add Yelp-specific fields:
    #transactions = Column(JSON, nullable=True)  # List of strings like ['pickup', 'delivery']
    operating_hours = Column(JSON, nullable=True)  # JSON object for opening hours
    attributes = Column(JSON, nullable=True)  # JSON object for attributes like open24h, waitlist etc.

    # Relationships
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    location = relationship("Location", back_populates="restaurants")

    #categories = relationship("RestaurantCategory", back_populates="restaurant")
    # Relationship to association objects
    restaurant_categories = relationship("RestaurantCategory", back_populates="restaurant", cascade="all, delete-orphan")
    # Convenient access to categories via association objects, read-only
    categories = relationship("Category", secondary="restaurant_categories", viewonly=True, back_populates="restaurants")

    foods = relationship("Food", back_populates="restaurant")
    operating_hours = relationship("OperatingHours", back_populates="restaurant", cascade="all, delete")
    reviews = relationship("Review", back_populates="restaurant")
    reservations = relationship("Reservation", back_populates="restaurant")
    photos = relationship("Photo", back_populates="restaurant")

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    #description = Column(String)
    type = Column(String)  # New field: e.g., 'cuisine', 'style', 'scenario'
    alias = Column(String, unique=True, nullable=False)  # ← Add this
    parent = Column(String)                # ← Optional

    restaurant_categories = relationship("RestaurantCategory", back_populates="category", cascade="all, delete-orphan")
    restaurants = relationship("Restaurant", secondary="restaurant_categories", viewonly=True, back_populates="categories")

    __table_args__ = (UniqueConstraint("alias", name="uix_category_alias"),)    

class RestaurantCategory(Base):
    __tablename__ = "restaurant_categories"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    category_id = Column(Integer, ForeignKey("categories.category_id"))

    restaurant = relationship("Restaurant", back_populates="restaurant_categories")
    category = relationship("Category", back_populates="restaurant_categories")
    #foods = relationship("Food", back_populates="restaurant")

    __table_args__ = (UniqueConstraint("restaurant_id", "category_id", name="uix_restaurant_category"),)

class Food(Base):
    __tablename__ = "foods"
    food_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)

    restaurant = relationship("Restaurant", back_populates="foods")
    category = relationship("Category")
    #reviews = relationship("Review", back_populates="food")
    ## One-to-one relationship with CultureStory
    ##culture_story = relationship("CultureStory", back_populates="food", uselist=False)

class CultureStory(Base):
    __tablename__ = "culture_stories"

    story_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Define a real sequence for food_id
    food_id_seq = Sequence("food_id_seq", start=1, increment=1)
    food_id = Column(Integer, food_id_seq, server_default=food_id_seq.next_value(), unique=True, index=True, nullable=False)

    food_name = Column(String, nullable=False)
    image_url = Column(String)
    origin_country = Column(String, nullable=True)
    story_summary = Column(String, nullable=True)  # Optional summary
    story = Column(String, nullable=True)

    #food = relationship("Food", back_populates="culture_story")

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    #food_id = Column(Integer, ForeignKey("foods.food_id"), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    #food = relationship("Food", back_populates="reviews")

class Reservation(Base):
    __tablename__ = "reservations"
    reservation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    reservation_time = Column(DateTime, nullable=False)
    party_size = Column(Integer)
    status = Column(String, default="confirmed")  # confirmed, canceled, etc.

    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")

class Favorite(Base):
    __tablename__ = "favorites"
    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=True)
    #food_id = Column(Integer, ForeignKey("foods.food_id"), nullable=True)

    user = relationship("User", back_populates="favorites")
    restaurant = relationship("Restaurant")
    #food = relationship("Food")

class Photo(Base):
    __tablename__ = "photos"
    photo_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    url = Column(String, nullable=False)
    caption = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="photos")
    user = relationship("User", back_populates="photos")

class OperatingHours(Base):
    __tablename__ = "operating_hours"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    day_of_week = Column(Integer)  # 0=Monday ... 6=Sunday
    open_time = Column(String)     # store as 'HHMM' or time type
    close_time = Column(String)
    is_overnight = Column(Boolean, default=False)

    location = relationship("Location", back_populates="operating_hours")

    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    restaurant = relationship("Restaurant", back_populates="operating_hours")
    __table_args__ = (
        UniqueConstraint("restaurant_id","location_id", "day_of_week", "open_time", "close_time", name="uix_operating_hours"),
    )

class TransactionType(Base):
    __tablename__ = "transaction_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(Float)
    payment_method = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String)