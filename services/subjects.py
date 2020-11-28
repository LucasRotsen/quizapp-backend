from tortoise.exceptions import IntegrityError

from database.models import Subject, Subject_Pydantic, Subject_Pydantic_List
from api.exceptions import NotImplementedException, SubjectAlreadyExistsException


async def get(subject_id=None):
    if not subject_id:
        subjects = await Subject_Pydantic_List.from_queryset(Subject.all())
        return subjects.dict().get('__root__')

    subject = await Subject_Pydantic.from_queryset_single(Subject.get(id=subject_id))
    return subject


async def create(subject):
    try:
        subject_obj = await Subject.create(**subject.dict(exclude_unset=True))
        return await Subject_Pydantic.from_tortoise_orm(subject_obj)

    except IntegrityError:
        raise SubjectAlreadyExistsException
    except Exception:
        raise NotImplementedException
