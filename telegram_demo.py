'''
Telegram Bot
Bot name: Marcus
Username: aka_Marcus_bot
'''
from pathlib import Path
import logging
import telebot

work_dir = Path(__file__).parent
with open(f"{work_dir}/login_info/aka_Marcus_bot.txt") as file:
    for index, word in enumerate(file):
        if index == 3:
            BOT_TOKEN = word.strip()
        else:
            pass

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    logging.info(call)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user = bot.get_me()
    print(user)
    bot.infinity_polling()