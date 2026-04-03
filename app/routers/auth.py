from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import User
from app.ouath2 import create_token
from app.schemas import Login, Token, UserCreate, UserResponse
from app.util import hash_password
from app.util import verify_password


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    user_data = user.model_dump(exclude={"password"})
    user_data["hashed_password"] = hash_password(user.password)
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(credential: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credential.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not verify_password(credential.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_token(payload={"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }

