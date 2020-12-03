import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#######################################################################################
#                              PROJECT VARIABLES                                      #
#######################################################################################

SECRET_KEY: str = os.getenv("SECRET_KEY")
HASHING_ALGORITHM: str = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES: float = float(os.getenv("TOKEN_EXPIRE_MINUTES"))

#######################################################################################
#                              CORS CONFIGURATION                                     #
#######################################################################################

ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]
