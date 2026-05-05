from jose import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY,ALGORITHM

def createAccessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)