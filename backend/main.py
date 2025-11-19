from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from core import models, schemas
from core.database import engine, SessionLocal, Base

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Satellite Anomaly Detection Backend")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test route to create a user
@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Test route to get all users
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
