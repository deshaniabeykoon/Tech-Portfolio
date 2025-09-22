# cuisine_compass/backend/auth/jwt_handler.py

from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

# Define default expiry time (e.g., 30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

def create_token(data: dict, secret: str, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

def decode_token(token: str, secret: str):
    return jwt.decode(token, secret, algorithms=[ALGORITHM])
