from loguru import logger
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from database import database_config


def init(app: FastAPI):
    """Init database and etc."""
    init_db(app)


def init_db(app: FastAPI):
    """
    Init database models.
    :param app:
    :return:
    """
    register_tortoise(
        app,
        db_url=database_config.db_url,
        generate_schemas=database_config.generate_schemas,
        modules=database_config.modules,
    )
