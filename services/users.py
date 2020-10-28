from tortoise.exceptions import DoesNotExist, OperationalError

from database.models import User, User_Pydantic, UserIn_Pydantic


async def get_user(username: str, fetch_password: bool = False) -> User_Pydantic:
    try:
        if fetch_password:
            user = await UserIn_Pydantic.from_queryset_single(User.get(username=username))
        else:
            user = await User_Pydantic.from_queryset_single(User.get(username=username))
        return user
    except DoesNotExist:
        raise NotImplementedError('Should throw a useful HTTP exception.')


async def create_user(user: UserIn_Pydantic) -> User_Pydantic:
    try:
        user_obj = await User.create(**user.dict(exclude_unset=True))
        return await User_Pydantic.from_tortoise_orm(user_obj)
    except OperationalError:
        raise NotImplementedError('Should throw a useful HTTP exception.')
