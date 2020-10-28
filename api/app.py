import uvicorn
from loguru import logger
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas import Token
from api.initializer import init
from services.users import create_user
from api.exceptions import IncorrectUsernameOrPassword
from database.models import User_Pydantic, UserIn_Pydantic
from security.authentication import authenticate_user, create_access_token, get_current_active_user

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


@app.post("/sign-up", response_model=User_Pydantic)
async def sign_up(user: UserIn_Pydantic):
    return await create_user(user)


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise IncorrectUsernameOrPassword

    access_token = create_access_token(data={"sub": user.username})

    logger.info(f'User {form_data.username} logged in.')
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/users/me/", response_model=User_Pydantic)
async def read_users_me(current_user: User_Pydantic = Depends(get_current_active_user)):
    return current_user


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
