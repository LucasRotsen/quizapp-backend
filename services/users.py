from tortoise.exceptions import DoesNotExist, IntegrityError

from database.models import User, User_Pydantic, UserIn_Pydantic
from api.exceptions import NotImplementedException, UserAlreadyExistsException


async def get(username: str, fetch_password: bool = False) -> User_Pydantic:
    try:
        if fetch_password:
            user = await UserIn_Pydantic.from_queryset_single(User.get(username=username))
        else:
            user = await User_Pydantic.from_queryset_single(User.get(username=username))
        return user

    except DoesNotExist:
        raise NotImplementedException


async def create(user: UserIn_Pydantic) -> User_Pydantic:
    try:
        user_obj = await User.create(**user.dict(exclude_unset=True))
        return await User_Pydantic.from_tortoise_orm(user_obj)

    except IntegrityError:
        raise UserAlreadyExistsException
    except Exception:
        raise NotImplementedException
