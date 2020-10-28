from dotenv import find_dotenv
from pydantic import Field, BaseSettings

DB_MODELS: list = ["database.models"]

MYSQL_DB_URL: str = "mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"


class MySQLSettings(BaseSettings):
    """MySQL env values"""
    mysql_user: str = Field(..., env="MYSQL_USER")
    mysql_password: str = Field(..., env="MYSQL_PASSWORD")
    mysql_host: str = Field(..., env="MYSQL_HOST")
    mysql_port: str = Field(..., env="MYSQL_PORT")
    mysql_db: str = Field(..., env="MYSQL_DB")


class TortoiseSettings(BaseSettings):
    """Tortoise-ORM settings"""

    db_url: str
    modules: dict
    generate_schemas: bool

    @classmethod
    def generate(cls):
        """Generate Tortoise-ORM settings"""

        mysql = MySQLSettings(_env_file=find_dotenv(), _env_file_encoding='utf-8')
        db_url = MYSQL_DB_URL.format(**mysql.dict())
        del mysql

        modules = {"models": DB_MODELS}
        return TortoiseSettings(db_url=db_url, modules=modules, generate_schemas=True)
