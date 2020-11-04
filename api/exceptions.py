from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_501_NOT_IMPLEMENTED


class NotImplementedException(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=HTTP_501_NOT_IMPLEMENTED,
            detail="Exception handling yet to be implemented."
        )


class IncorrectUsernameOrPasswordException(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class SubjectAlreadyExistsException(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Subject already exists"
        )


class UserAlreadyExistsException(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="User already exists"
        )


class InvalidCredentialsException(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            headers={"WWW-Authenticate": "Bearer"},
            detail='Could not validate credentials',
        )


class InactiveUserException(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Inactive user',
        )
