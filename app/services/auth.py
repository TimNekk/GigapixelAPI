from fastapi import Request, HTTPException, status

from app.crud import get_token


def verify_token(req: Request):
    token = req.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    db_token = get_token(token)
    if not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

    return db_token
