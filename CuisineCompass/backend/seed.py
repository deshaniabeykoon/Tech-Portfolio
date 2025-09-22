import csv
from cuisine_compass.backend.models import Food, Restaurant, CultureStory
from cuisine_compass.backend.database.database import SessionLocal

db = SessionLocal()

with open('imports/foodsRestaurent1.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        food = Food(
            restaurant_id=1,
            name=row['name'],
            description=row.get('description'),
            price=float(row['price']) if row.get('price') else None,
            category_id=int(row['category_id']) if row.get('category_id') else None
        )
        db.add(food)
        db.flush()  # Flush after each insert to avoid memory issues

        if row.get('country') and row.get('story'):
            culture_story = CultureStory(
                food_id=food.food_id,
                country=row['country'],
                story=row['story']
            )
            db.add(culture_story)

# with open('data/sample_restaurants.csv') as f:
#     for row in csv.DictReader(f):
#         db.add(Restaurant(
#             name=row['name'],
#             location=row['location'],
#             latitude=float(row['latitude']),
#             longitude=float(row['longitude']),
#             cuisine_type=row['cuisine']
#         ))
db.commit()