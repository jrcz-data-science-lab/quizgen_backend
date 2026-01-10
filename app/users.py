from sqlalchemy.orm import Session
from . import models
from .schemas import UserCreate
from .auth import hash_password, verify_password
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(user: UserCreate, db: Session):
    hashed_pw = hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user
