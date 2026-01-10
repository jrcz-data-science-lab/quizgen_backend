from fastapi import FastAPI, Depends, HTTPException
from .schemas import UserCreate, LoginData
from .database import Base, engine
from .auth import create_access_token, get_current_supabase_user
from .users import get_db, create_user, authenticate_user


app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


@app.post("/register")
def register(user: UserCreate, db=Depends(get_db)):
    new_user = create_user(user, db)
    return {"message": "User created successfully", "user_id": new_user.id}


@app.post("/login")
def login(login_data: LoginData, db=Depends(get_db)):
    user = authenticate_user(login_data.email, login_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email,
        "id": user.id
    }

@app.get("/me")
def get_me(current_user=Depends(get_current_supabase_user)):
    """Return the Supabase authenticated user info (protected endpoint)."""
    return {"user": current_user}

