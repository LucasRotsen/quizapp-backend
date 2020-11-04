from tortoise.exceptions import IntegrityError

from database.models import Quiz, Question
from api.exceptions import NotImplementedException


async def create(quiz_data, user_data):
    try:
        quiz = await Quiz.create(title=quiz_data.title,
                                 description=quiz_data.description,
                                 creator_id=user_data.id)

        for question in quiz_data.questions:
            question = await Question.create(**question.dict(exclude_unset=True))
            await quiz.questions.add(question)

        return quiz.id

    except IntegrityError:
        raise NotImplementedException
