'''
package for telegram bot
'''
import logging
from openai_api import ChatOpenAPI
from database_for_bot import CassandraDB
from .telegram_bot_config import bot
from .telegram_register import *
from .telegram_openai import *

@bot.message_handler(commands=['start'])
def command_hello(message):
    logging.info("receive hello command")
    msg = "Hello! I'm a bot\nPlease Submit '/help' to get user manual"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['help'])
def command_help(message):
    logging.info("receive help command")
    msg = (
        "This is a help message\n\n"
        "/start : will send you Welcome message\n"
        "/help : will send you this message\n"
        "/register : register a new account\n"
        "check or info : display your account information\n"
        "/openai : answer your question about rule\n"
        "In addition to the above, he will reply you with the exact same sentence\n"
    )
    bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    '''
    check the command is activate or not
    if not, echo the message
    '''
    logging.info(f"receive echo message\n{message.text}")
    bot.reply_to(message, message.text)
