from fastapi import HTTPException, status


subscribe_already_exist = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="subscribe already exist or wrong user id",
)
