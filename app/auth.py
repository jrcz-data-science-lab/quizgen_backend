from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
import requests
from fastapi import HTTPException, Depends, Request

from typing import Any, Dict

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_supabase_token(access_token: str):
    """Verify a Supabase access token by calling the Supabase Auth user endpoint.

    Returns user info dict on success, or raises HTTPException(401) on failure.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    if not supabase_url:
        raise RuntimeError("SUPABASE_URL not set in environment")

    url = f"{supabase_url.rstrip('/')}/auth/v1/user"
    headers = {"Authorization": f"Bearer {access_token}"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired Supabase token")

    return resp.json()


def get_current_supabase_user(request: Request) -> Dict[str, Any]:
    """FastAPI dependency to extract and verify Supabase access token from Authorization header.

    Usage: `user = Depends(get_current_supabase_user)` in route signature.
    Returns the Supabase user JSON object on success.
    """
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = parts[1]
    user = verify_supabase_token(token)
    return user
