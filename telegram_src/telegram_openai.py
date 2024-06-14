
import logging
from .telegram_bot_config import bot
from . import ChatOpenAPI

print("Module telegram_openai loaded")

@bot.message_handler(commands=['openai'])
def command_openai(message):
    bot.send_message(message.chat.id, "你對規定有甚麼樣的問題嗎??")
    bot.register_next_step_handler(message, handle_openai)

def handle_openai(message):
    chat_id = message.chat.id
    answer = ChatOpenAPI(message.text).main()
    logging.info(f"question is {message.text}")
    logging.info(f"answer is {answer}")
    bot.send_message(chat_id, answer)