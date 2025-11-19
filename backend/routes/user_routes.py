from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core import schemas, crud
from core.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new user
@router.post("/users/", response_model=schemas.UserCreate)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# Get all users
@router.get("/users/", response_model=list[schemas.UserCreate])
def get_users_route(db: Session = Depends(get_db)):
    return crud.get_users(db)

# Get user by ID
@router.get("/users/{user_id}", response_model=schemas.UserCreate)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
