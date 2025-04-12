from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

# Import your models and other components
from models import User, Base
import schemas
import auth
from crud import create_user, get_user, get_users, update_user, delete_user
from database import SessionLocal, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration endpoint
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

# Login endpoint
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User CRUD endpoints
@app.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db=db, user_id=user_id)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user_endpoint(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    return update_user(db=db, user_id=user_id, user_data=user)

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db=db, user_id=user_id)
