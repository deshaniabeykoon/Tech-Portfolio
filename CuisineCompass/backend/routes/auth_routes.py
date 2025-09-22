from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models import User
from backend.auth.auth import verify_password, create_access_token, get_current_user

auth_router = APIRouter()

@auth_router.post("/login", summary="Use user email to login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    #access_token = create_access_token(data={"sub": user.user_id})
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/logout")
def logout():
    # JWT-based logout is usually done client-side (discard token).
    # Optionally, implement server-side token blacklisting.
    return {"message": "Successfully logged out. Please discard the token client-side."}

@auth_router.get("/admin-only")
def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"secret": "admin-data"}

