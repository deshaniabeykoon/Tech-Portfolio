# 🌏 Multicultural Cuisine Compass

A culturally enriched restaurant discovery platform powered by AI. Users can browse diverse restaurants, explore cultural food stories, rate/review their experiences, and receive personalized recommendations.

---

## 📦 Features

- 🔐 **User Authentication** (JWT-based)
  - Register / Login / Logout
  - Admin-only protected routes
- 🍽️ **Restaurants**
  - Browse restaurants with filters (cuisine, scene, diet)
  - View details, operating hours, and real-time data
- ⭐ **Reviews & Ratings**
  - Submit one review per restaurant
  - Moderation via AI sentiment and toxicity checks
- ❤️ **Favorites**
  - Add/remove favorite restaurants
- 📖 **Cultural Food Stories**
  - Auto-generated with LLMs (OpenAI, DeepSeek, HuggingFace)
  - Origins, traditions, and fun facts
- 🧭 **Cultural Journey Route**
  - AI-generated food trails across cultures
- 🧠 **Personalized Recommendations**
  - Suggests restaurants based on user's history/preferences
- 🤖 **AI Assistant**
  - Chat for cultural Q&A or recommendations

---

## 🛠️ Tech Stack

| Layer           | Tech                             |
|-----------------|----------------------------------|
| Backend         | **FastAPI**                      |
| ORM             | SQLAlchemy                       |
| Database        | PostgreSQL                       |
| Auth            | JWT + OAuth2 + bcrypt            |
| LLM Providers   | DeepSeek                         |
| Scheduler       | APScheduler (daily tasks)        |
| External APIs   | Yelp Fusion API                  |

---

## 🗂️ Project Structure

```
cuisine_compass/
├── backend/
│   ├── app.py                   # FastAPI main app
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── routes/                  # API route files
│   ├── services/                # Business logic & integrations
│   ├── database/                # DB connection (Singleton)
│   ├── auth/                    # JWT, password hashing, roles
│   ├── scheduler.py             # LLM background jobs
│   └── seed.py                  # Initial data importer
```

---

## 🚀 Running the App

### 1. Clone the repo
```bash
git clone https://gitlab.com/cusinecompass/CusineCompass.git
cd cuisine_compass
```

### 2. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file with:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cuisine_compass
DB_USER=postgres
DB_PASSWORD=your_password
SECRET_KEY=supersecretkey
YELP_API_KEY=your_yelp_api_key
TOGETHER_API_KEY=your_llm_api_key
```

### 5. Start the server
```bash
uvicorn backend.app:app --reload
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Sample Endpoints

| Action                        | Endpoint                            |
|------------------------------|-------------------------------------|
| Register User                | `POST /users/register`              |
| Login                        | `POST /login`                       |
| Browse Restaurants           | `GET /restaurants/browse`           |
| Submit Review                | `POST /reviews/addReview/`          |
| View Food Stories            | `GET /foods/cultural-stories`       |
| Generate Restaurant Summary  | `POST /restaurants/generate-summary/{id}` |
| AI Chat Assistant            | `POST /ai/chat`                     |

---

## 🧠 AI & LLM Integration

- Uses `together.ai`, `HuggingFace`, or `OpenAI` for:
  - Summarizing restaurant themes
  - Generating cultural food stories
  - Personalized recommendations
  - Moderating toxic or biased reviews

---

## 🧩 Design Patterns Used

- **Singleton**: `DatabaseConnection` class
- **Factory**: `LLMFactory` for selecting LLM providers
- **Service Layer**: All `services/` handle logic separate from routes

---

## 👥 Contributors

- Euphrashia Abeykoon — Backend, API, AI Integration  
- Xinyi Zhao — Frontend, Testing, Scrum Master

---

## 📄 License

MIT License © 2025 Cuisine Compass Team