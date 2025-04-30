from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import get_db
from .models import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register/")
def register(username: str, password: str, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(password)
    user = User(username=username, hashed_password=hashed_pwd)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
