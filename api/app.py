import uvicorn
from loguru import logger
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from api.exceptions import IncorrectUsernameOrPassword
from database.models import fake_users_db, Token, User
from security.authentication import authenticate_user, create_access_token, get_current_active_user

app = FastAPI(
    title='QuizApp API',
    description='RESTful API for Quiz / Trivia management',
    version='0.0.1',
    docs_url='/documentation',
    redoc_url=None,
)


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise IncorrectUsernameOrPassword

    access_token = create_access_token(data={"sub": user.username})

    logger.info(f'User {form_data.username} logged in.')
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
