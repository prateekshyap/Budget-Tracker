# app/api/routes.py

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat()
    }

@router.get("/test")
def test_api():
    return {"message": "API is working"}
