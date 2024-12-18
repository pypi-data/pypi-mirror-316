import logging

from fastapi import FastAPI

from lib.websockets import setup_app

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X')

logger = logging.getLogger(__name__)
SECRET_KEY = "your_secret_key"

app = FastAPI()

app = setup_app(
    app=app,
    base_path='/ws',
    jwt_secret_key=SECRET_KEY,
)
