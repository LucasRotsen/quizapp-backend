from tortoise.models import Model
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from security.authentication import get_password_hash


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=False)
    username = fields.CharField(max_length=20, unique=True, null=False)
    password = fields.CharField(max_length=100, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    quizzes: fields.ReverseRelation["Quiz"]

    answers: fields.ManyToManyRelation["QuizQuestion"] = fields.ManyToManyField(
        model_name="models.QuizQuestion",
        related_name="respondents",
        through="answers",
        backward_key="respondent_id",
        forward_key="quiz_question_id",
    )

    async def save(self, *args, **kwargs) -> None:
        self.password = get_password_hash(self.password)
        await super().save(*args, **kwargs)

    class Meta:
        table = "users"
        ordering = ["created_at"]

    class PydanticMeta:
        exclude = ("created_at",)


class Quiz(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    questions: fields.ManyToManyRelation["Question"] = fields.ManyToManyField(
        model_name="models.Question",
        related_name="quizzes",
        through="quiz_questions",
        backward_key="quiz_id",
        forward_key="question_id",
    )

    creator: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        model_name="models.User",
        related_name="quizzes"
    )

    def created_date(self) -> str:
        """
        Formats `created_date` in a more readable way
        """
        return f"{self.created_at:%d/%m/%Y}"

    class Meta:
        table = "quizzes"
        computed = ["created_date"]

    class PydanticMeta:
        computed = ["created_date"]
        exclude = ("created_at", "quiz_questionss", "creator",)


class Question(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    alternative_a = fields.CharField(max_length=100, null=True)
    alternative_b = fields.CharField(max_length=100, null=True)
    alternative_c = fields.CharField(max_length=100, null=True)
    alternative_d = fields.CharField(max_length=100, null=True)
    answer = fields.CharField(max_length=1, null=True)

    subject: fields.ForeignKeyNullableRelation["Subject"] = fields.ForeignKeyField(
        model_name="models.Subject",
        related_name="questions"
    )

    class Meta:
        table = "questions"

    class PydanticMeta:
        exclude = ("quiz_questionss", "answer",)


class QuizQuestion(Model):
    id = fields.IntField(pk=True)

    respondents: fields.ManyToManyRelation["User"]
    quiz: fields.ForeignKeyRelation["Quiz"] = fields.ForeignKeyField(model_name="models.Quiz")
    question: fields.ForeignKeyRelation["Question"] = fields.ForeignKeyField(model_name="models.Question")

    class Meta:
        table = "quiz_questions"


class Answer(Model):
    id = fields.IntField(pk=True)
    answer = fields.CharField(max_length=50, null=True)
    is_correct = fields.BooleanField(default=0)

    respondent = fields.ForeignKeyField(model_name="models.User")
    quiz_question = fields.ForeignKeyField(model_name="models.QuizQuestion")

    class Meta:
        table = "answers"


class Subject(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True, null=False)

    questions: fields.ReverseRelation["Question"]

    class Meta:
        table = "subjects"


Tortoise.init_models(["database.models"], "models")

User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password",))
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

Quiz_Pydantic = pydantic_model_creator(Quiz, name="Quiz")
QuizIn_Pydantic = pydantic_model_creator(Quiz, name="QuizIn", exclude_readonly=True)

Question_Pydantic = pydantic_model_creator(Question, name="Question")
QuestionIn_Pydantic = pydantic_model_creator(Question, name="QuestionIn", exclude_readonly=True)

QuizQuestion_Pydantic = pydantic_model_creator(Question, name="QuizQuestion")
QuizQuestionIn_Pydantic = pydantic_model_creator(Question, name="QuizQuestionIn", exclude_readonly=True)

Answer_Pydantic = pydantic_model_creator(Answer, name="Answer")
AnswerIn_Pydantic = pydantic_model_creator(Answer, name="AnswerIn", exclude_readonly=True)

Subject_Pydantic = pydantic_model_creator(Subject, name="Subject", exclude=("questions",))
SubjectIn_Pydantic = pydantic_model_creator(Subject, name="SubjectIn", exclude_readonly=True)
Subject_Pydantic_List = pydantic_queryset_creator(Subject, sort_alphabetically=True, exclude=("questions",))
