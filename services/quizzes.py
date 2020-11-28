from tortoise.exceptions import IntegrityError

from api.schemas import QuizReport, QuestionReport
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


async def answer(quiz_answer):
    count_correct = 0
    question_reports = []
    for question_answer in quiz_answer.answers:
        db_question = await Question.get(id=question_answer.id)

        answer_is_correct = (question_answer.answer == db_question.answer)
        if answer_is_correct:
            count_correct += 1

        question_reports.append(QuestionReport(answer=question_answer.answer,
                                               actual=db_question.answer,
                                               is_correct=answer_is_correct))

    quiz_score = f"{round((count_correct * 100) / len(quiz_answer.answers), 2)}%"
    return QuizReport(score=quiz_score, questions=question_reports)
