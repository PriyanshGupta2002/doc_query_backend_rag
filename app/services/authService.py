from sqlalchemy.orm import Session
from app.core.security import createAccessToken
from app.utils.passwordHashing import hashPassword,verifyPassword
from app.models.userModel import User


def registerUser(db:Session,name:str,email:str,password:str):
    hashedPassword = hashPassword(password=password)
    user = User(name=name,email=email,password=hashedPassword)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def loginUser(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    isPasswordGenuine = verifyPassword(password, hashed=user.password)

    if not isPasswordGenuine:
        return None

    token = createAccessToken({
        "sub": str(user.id)   # 👈 IMPORTANT: use user.id, not email
    })

    return token
    