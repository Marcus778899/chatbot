from pathlib import Path
from telebot import TeleBot

WORK_DIR = Path(__file__).parent.parent.absolute()
with open(f"{WORK_DIR}/login_info/Marcus_First_Bot.txt","r") as file:
    TOKEN = file.read().split('\n')[3]

# init telegram bot
bot = TeleBot(TOKEN,parse_mode=None)

print("start telegram app!!")