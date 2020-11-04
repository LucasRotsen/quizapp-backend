from typing import Optional, List

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class QuestionData(BaseModel):
    title: str
    description: Optional[str]
    alternative_a: Optional[str]
    alternative_b: Optional[str]
    alternative_c: Optional[str]
    alternative_d: Optional[str]
    answer: Optional[str]
    subject_id: Optional[int]


class QuizData(BaseModel):
    title: str
    description: Optional[str]
    questions: List[QuestionData]
