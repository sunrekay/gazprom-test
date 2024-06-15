from fastapi import HTTPException, status

user_not_exist = HTTPException(
    detail="user not exist",
    status_code=status.HTTP_401_UNAUTHORIZED,
)

user_already_exist = HTTPException(
    detail="user already exist",
    status_code=status.HTTP_403_FORBIDDEN,
)

wrong_email_or_password = HTTPException(
    detail="wrong email or password",
    status_code=status.HTTP_401_UNAUTHORIZED,
)
