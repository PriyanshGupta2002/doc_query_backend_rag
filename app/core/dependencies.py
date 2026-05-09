from fastapi import HTTPException, Cookie, Header
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM


def get_current_user(
    accessToken: str = Cookie(None),
    authorization: str = Header(None),
):
    token = None

    # Check Bearer token first
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]

    # Fallback to cookie
    elif accessToken:
        token = accessToken
        print("token",token)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Unauthenticated"
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )