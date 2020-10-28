from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from services import users
from api.schemas import TokenData, UserP
from api.exceptions import InvalidCredentialsException
from api.config import SECRET_KEY, HASHING_ALGORITHM, TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)

    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await users.get_user(username, fetch_password=True)

    if not verify_password(password, user.password):
        return False

    user.__delattr__('password')

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise InvalidCredentialsException

        token_data = TokenData(username=username)

    except JWTError:
        raise InvalidCredentialsException

    return await users.get_user(username=token_data.username)


async def get_current_active_user(current_user: UserP = Depends(get_current_user)):
    return current_user
