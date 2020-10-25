from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


class IncorrectUsernameOrPassword(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
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
