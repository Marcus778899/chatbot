import logging
from openai_api import ChatOpenAPI
from .linebot_config import *
from .answer_question import *

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")