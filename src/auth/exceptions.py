from fastapi import HTTPException, status

token_invalid = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid token",
)

token_expired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="expired token",
)
