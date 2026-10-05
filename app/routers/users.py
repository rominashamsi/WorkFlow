from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.core.database import engine
from app.core.security import hash_password, verify_password, create_access_token, get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, UserUpdate, PasswordUpdate

router = APIRouter()

class LoginForm:
    def __init__(
        self,
        username: str = Form(...,description="Username"),
        password: str = Form(...,description="Password")
    ):
        self.username = username
        self.password = password


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


@router.post("/login/", response_model=Token)
def login_user(form_data: LoginForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):

        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    return {"access_token": access_token,
             "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user




@router.put("/me", response_model=UserResponse)
def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_data.first_name is not None:
        current_user.first_name = user_data.first_name

    if user_data.last_name is not None:
        current_user.last_name = user_data.last_name

    db.commit()
    db.refresh(current_user)

    return current_user


@router.put("/me/password")
def update_my_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(
        password_data.current_password,
        current_user.password,
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect",
        )

    current_user.password = hash_password(
        password_data.new_password
    )

    db.commit()

    return {
        "message": "Password updated successfully"
    }


@router.delete("/me")
def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.delete(current_user)
    db.commit()

    return {
        "message": "Account deleted successfully"
    }



@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = db.query(User).all()

    return users



@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user

    