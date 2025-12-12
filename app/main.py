# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as api_router

app = FastAPI(title="Monthly Tracking Dashboard")

# Include API routes
app.include_router(api_router, prefix="/api")

# Serve static files (HTML, JS, CSS)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
