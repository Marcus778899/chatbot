'''
package for telegram bot
'''
import logging
from openai_api import ChatOpenAPI
from database_for_bot import CassandraDB
from .telegram_bot_config import bot
from .telegram_register import *
from .telegram_openai import *

logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['hello'])
def command_hello(message):
    logging.info("receive hello command")
    msg = "Hello! I'm a bot\nPlease Submit '/start' to get start"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    '''
    check the command is activate or not
    if not, echo the message
    '''
    logging.info(f"receive echo message\n{message.text}")
    bot.reply_to(message, message.text)
