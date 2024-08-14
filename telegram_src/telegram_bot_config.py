from configparser import ConfigParser
import os
from telebot import TeleBot

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__),'telegramInfo.cfg'))
TOKEN = config.get('LOGIN', 'TOKEN')
# init telegram bot
bot = TeleBot(TOKEN,parse_mode=None)

print("start telegram app!!")