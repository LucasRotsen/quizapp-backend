from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

from security.authentication import get_password_hash


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=False)
    username = fields.CharField(max_length=20, unique=True, null=False)
    password = fields.CharField(max_length=100, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    quizzes: fields.ReverseRelation["Quiz"]
    answers: fields.ReverseRelation["Answer"]

    async def save(self, *args, **kwargs) -> None:
        self.password = get_password_hash(self.password)
        await super().save(*args, **kwargs)

    class Meta:
        table = "users"
        ordering = ["created_at"]

    class PydanticMeta:
        exclude = ["created_at"]


class Quiz(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    creator: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User",
        related_name="quizzes",
        to_field="id",
        on_delete=fields.CASCADE
    )
    questions: fields.ManyToManyRelation["Question"] = fields.ManyToManyField(
        model_name="models.Question",
        related_name="quizzes",
        through="quiz_question"
    )

    def created_date(self) -> str:
        """
        Formats `created_date` in a more readable way
        """
        return f"{self.created_at:%d/%m/%Y}"

    class Meta:
        table = "quizzes"
        computed = ["created_date"]


class Question(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    answer = fields.CharField(max_length=150, null=True)
    answer_description = fields.CharField(max_length=200, null=True)

    quizzes: fields.ManyToManyRelation[Quiz]
    answers: fields.ReverseRelation["Question"]
    subject: fields.ForeignKeyNullableRelation["Subject"] = fields.ForeignKeyField(
        model_name="models.Subject",
        related_name="questions",
        to_field="id"
    )

    class Meta:
        table = "questions"


class Answer(Model):
    id = fields.IntField(pk=True)
    answer = fields.CharField(max_length=50, null=True)
    is_correct = fields.BooleanField(default=0)

    respondent: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User",
        related_name="answers",
        to_field="id",
        on_delete=fields.CASCADE
    )
    question: fields.ForeignKeyRelation[Question] = fields.ForeignKeyField(
        model_name="models.Question",
        related_name="answers",
        to_field="id",
        on_delete=fields.CASCADE
    )

    class Meta:
        table = "answers"
        unique_together = (("respondent", "question"),)


class Subject(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True, null=False)

    questions: fields.ReverseRelation[Question]

    class Meta:
        table = "subjects"


User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password",))
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

Quiz_Pydantic = pydantic_model_creator(Quiz, name="Quiz")
QuizIn_Pydantic = pydantic_model_creator(Quiz, name="QuizIn", exclude_readonly=True)

Question_Pydantic = pydantic_model_creator(Question, name="Question")
QuestionIn_Pydantic = pydantic_model_creator(Question, name="QuestionIn", exclude_readonly=True)

Answer_Pydantic = pydantic_model_creator(Answer, name="Answer")
AnswerIn_Pydantic = pydantic_model_creator(Answer, name="AnswerIn", exclude_readonly=True)

Subject_Pydantic = pydantic_model_creator(Subject, name="Subject")
SubjectIn_Pydantic = pydantic_model_creator(Answer, name="SubjectIn", exclude_readonly=True)
