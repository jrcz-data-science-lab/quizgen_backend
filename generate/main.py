import json, re, requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.mcqroutes import router as mcq_router
from services import get_services

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(mcq_router, prefix="/generate")

@app.get("/")
def root():
    return {"message": "Backend running"}
