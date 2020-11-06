from tortoise.exceptions import IntegrityError

from api.exceptions import NotImplementedException
from database.models import Quiz, Question, Quiz_Pydantic


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
