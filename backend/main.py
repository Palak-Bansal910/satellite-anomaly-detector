from fastapi import FastAPI
from core.database import engine, Base

# Import routers
from routes.anomaly_routes import router as anomaly_router
from routes.user_routes import router as user_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Satellite Anomaly Detection Backend")

# Include routers
app.include_router(user_router)      # Routes for User table
app.include_router(anomaly_router)   # Routes for Anomaly table

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "Backend is running!"}
