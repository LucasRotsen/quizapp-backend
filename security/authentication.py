from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from services.users import get_user
from database.models import fake_users_db, TokenData, User
from api.config import SECRET_KEY, HASHING_ALGORITHM, TOKEN_EXPIRE_MINUTES
from api.exceptions import InvalidCredentialsException, InactiveUserException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise InvalidCredentialsException

        token_data = TokenData(username=username)

    except JWTError:
        raise InvalidCredentialsException

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise InvalidCredentialsException

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise InactiveUserException

    return current_user
