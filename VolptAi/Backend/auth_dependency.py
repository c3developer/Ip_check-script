from jose import jwt

from fastapi import Header
from fastapi import HTTPException

from config import (
    SECRET_KEY,
    ALGORITHM
)


def get_current_username(
        authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["sub"]

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )