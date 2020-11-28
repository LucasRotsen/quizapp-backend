from tortoise.exceptions import IntegrityError

from api.exceptions import NotImplementedException
from database.models import Quiz, Question, Quiz_Pydantic, Quiz_Pydantic_List


async def get(quiz_id=None):
    if not quiz_id:
        quizzes = await Quiz_Pydantic_List.from_queryset(Quiz.all())
        return quizzes.dict().get('__root__')

    subject = await Quiz_Pydantic.from_queryset_single(Quiz.get(id=quiz_id))
    return subject


async def create(quiz_data, user_data):
    try:
        quiz = await Quiz.create(title=quiz_data.title,
                                 description=quiz_data.description,
                                 creator_id=user_data.id)

        for question in quiz_data.questions:
            question = await Question.create(**question.dict(exclude_unset=True))
            await quiz.questions.add(question)

        return await Quiz_Pydantic.from_tortoise_orm(quiz)

    except IntegrityError:
        raise NotImplementedException
