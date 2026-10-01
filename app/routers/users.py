from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import engine
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):


    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")


    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hash_password(user.password),
        role="member",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user