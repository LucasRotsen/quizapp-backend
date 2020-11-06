import uvicorn
from loguru import logger
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from api.initializer import init
from api.schemas import Token, QuizData
from services import users, quizzes, subjects
from api.exceptions import IncorrectUsernameOrPasswordException
from security.authentication import authenticate_user, create_access_token, get_current_user
from database.models import User_Pydantic, UserIn_Pydantic, Subject_Pydantic, SubjectIn_Pydantic, Quiz_Pydantic

app = FastAPI(
    title='QuizApp API',
    description='RESTful API for Quiz / Trivia management',
    version='0.0.1',
    docs_url='/documentation',
    redoc_url=None,
)


@app.on_event('startup')
async def init_database_orm():
    init(app)


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise IncorrectUsernameOrPasswordException

    access_token = create_access_token(data={"sub": user.username})

    logger.info(f'User {form_data.username} logged in.')
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/sign-up", response_model=User_Pydantic)
async def sign_up(user: UserIn_Pydantic):
    user = await users.create(user)

    logger.info(f'User {user.id} created!')
    return user


@app.post("/subjects/create", response_model=Subject_Pydantic)
async def create_subject(subject: SubjectIn_Pydantic, current_user: User_Pydantic = Depends(get_current_user)):
    subject = await subjects.create(subject)

    logger.info(f'Subject #{subject.id} created!')
    return subject


@app.post("/quizzes/create", response_model=Quiz_Pydantic)
async def create_quiz(quiz_data: QuizData, current_user: User_Pydantic = Depends(get_current_user)):
    quiz = await quizzes.create(quiz_data, current_user)

    logger.info(f'Quiz #{quiz.id} created!')
    return quiz


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
