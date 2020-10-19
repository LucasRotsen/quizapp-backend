import json
import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI(
    title="Quiz App - Backend",
    description="Rest API for Quiz management",
    version="0.0.1",
    redoc_url='/documentation',
    docs_url=None
)


@app.get('/hello-echo/{text}')
def hello_echo(text: str) -> Response:
    message = f'Hello, {text}!'

    logger.info(message)
    return Response(
        json.dumps({'text': message}),
        media_type='application/json'
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
