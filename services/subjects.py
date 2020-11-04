from tortoise.exceptions import IntegrityError

from database.models import Subject, Subject_Pydantic
from api.exceptions import NotImplementedException, SubjectAlreadyExistsException


async def create(subject):
    try:
        subject_obj = await Subject.create(**subject.dict(exclude_unset=True))
        return await Subject_Pydantic.from_tortoise_orm(subject_obj)

    except IntegrityError:
        raise SubjectAlreadyExistsException
    except Exception:
        raise NotImplementedException
