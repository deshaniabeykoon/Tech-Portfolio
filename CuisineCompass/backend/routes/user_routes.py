from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from backend.database.database import get_db, get_session
from backend.models import User
from backend.schemas import UserResponse, UserRegister
from typing import List
from backend.auth.auth import *
from passlib.hash import bcrypt

router = APIRouter()

@router.get("/all", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_session),
    current_admin: User = Depends(admin_required),
):
    users = db.query(User).all()
    return users
# def list_users(db: Session = Depends(get_session)):
#     users = db.query(User).all()
#     if not users:
#         raise HTTPException(status_code=404, detail="No users found")
#     return users

# Users Can View Only Their Own Data (and admins can view anyone’s)
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin" and current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.user_id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_session)):
    # Check for duplicate email
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check for duplicate username
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Enforce password strength
    validate_password_strength(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=bcrypt.hash(user.password),
        role="user"  # default role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/admin/dashboard")
def admin_dashboard(admin_user: User = Depends(get_current_admin_user)):
    return {"message": f"Welcome, Admin {admin_user.username}!"}