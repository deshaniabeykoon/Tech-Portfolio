from backend.auth.jwt_handler import create_token
from backend.utils.env import SECRET_KEY  # loaded via dotenv
from backend.schemas import *
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.auth.auth import *  # Make sure this import path is correct
import logging

from cuisine_compass.backend.database.database import get_session

def login_user(request: LoginRequest, db: Session = Depends(get_session)):
    #user = authenticate_user(email, password, db)
    user = authenticate_user_by_email(request.user_email, request.password, db)
    if not user:
        logging.warning(f"Failed login attempt for {request.user_email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": user.email,
        "role": user.role,
        "user_id": user.user_id
    }
    access_token = create_token(token_data, secret=SECRET_KEY)
    return {"access_token": access_token, "token_type": "bearer"}
