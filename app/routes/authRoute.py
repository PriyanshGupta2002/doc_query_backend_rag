from fastapi import APIRouter, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from app.schemas.userSchema import UserCreate, UserLogin
from app.db.session import SessionLocal
from app.services.authService import registerUser, loginUser
from app.schemas.responseSchema import responseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register",response_model=responseModel)
def register(user: UserCreate, db: Session = Depends(get_db)):
    registeredUser =  registerUser(db, user.name,user.email, user.password)
    return responseModel(
        message="User registered successfully",
        success=True,
        data={"id": registeredUser.id, "email": registeredUser.email}
    )

@router.post("/login",response_model=responseModel)
def login(user: UserLogin,response:Response, db: Session = Depends(get_db)):
    token = loginUser(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    response.set_cookie(
        key="accessToken",
        value=token,
        httponly=True,
        samesite="lax"
    )
    return responseModel(
        message="Login successful",
        success=True,
        data={"access_token": token}
    )