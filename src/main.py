from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.models.item import Base
from src.database import engine
from src.routers import items
import os

app = FastAPI(title="Consumption Dashboard")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Register API routers
app.include_router(items.router, prefix="/api")

@app.get("/")
def read_dashboard():
    return FileResponse(os.path.join("app/static", "index.html"))