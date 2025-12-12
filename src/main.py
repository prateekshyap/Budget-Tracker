from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.models.item import Base
from src.database import engine
from src.routers import items

app = FastAPI(title="Consumption Dashboard")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Register API routers
app.include_router(items.router, prefix="/api")
app.include_router(items.router, prefix="/api/items")


# Serve the dashboard HTML
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
