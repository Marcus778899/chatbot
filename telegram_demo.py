'''
Telegram Bot
Bot name: Marcus
Username: aka_Marcus_bot
'''
from pathlib import Path
import logging
from telebot import types, TeleBot
from openai_api import ChatOpenAPI

work_dir = Path(__file__).parent
with open(f"{work_dir}/login_info/aka_Marcus_bot.txt") as file:
    for index, word in enumerate(file):
        if index == 3:
            BOT_TOKEN = word.strip()
        else:
            pass

bot = TeleBot(BOT_TOKEN, parse_mode=None)
user_dict = {}
class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.gender = None

# Handle /start
@bot.message_handler(commands=['start']) # prefix plus /
def send_welcome(message):
    logging.info(
        f"User {message.chat.last_name + message.chat.first_name} has started the bot"
    )
    msg = bot.reply_to(
        message, 
        f"Welcome to Register Account\nPlease enter your name"
        )
    bot.register_next_step_handler(msg, process_name)

def process_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, "How old are you?")
        bot.register_next_step_handler(msg, process_age)
    except Exception as e:
        bot.reply_to(message, "oooops name error")

def process_age(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, "Age should be a number. Enter your age again.")
            bot.register_next_step_handler(msg, process_age)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Male", "Female")
        msg = bot.reply_to(message, "What is your gender?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_gender)
    except Exception as e:
        bot.reply_to(message, "oooops age error")
        print(e)

def process_gender(message):
    try:
        chat_id = message.chat.id
        gender = message.text
        user = user_dict[chat_id]
        if (gender == "Male") or (gender == "Female"):
            user.gender = gender
        else:
            raise Exception("Invalid gender")
        bot.send_message(
            chat_id, 
            f"Thanks your register"
            )
        logging.info(
            f"register content is\n{user.__dict__}"
        )
    except Exception as e:
        bot.reply_to(message, "oooops gender error")
        logging.error(e)

@bot.message_handler(regexp="show") # Regular expression
def command_help(message):
    for index, value in user_dict.items():
        logging.info(f"index is {index} \n show content is {value.__dict__}")
        bot.send_message(
            index,
            f"Name: {value.name}\nAge: {value.age}\nGender: {value.gender}"
        )

@bot.message_handler(regexp="openai")
def command_openai(message):
    msg = bot.send_message(message.chat.id, "What is your question?")
    bot.register_next_step_handler(msg, process_openai)

def process_openai(message):
    chat_id = message.chat.id
    answer = ChatOpenAPI(message.text).main()
    logging.info(f'Question is {message.text}')
    logging.info(f"Answer is \n{answer}")
    bot.send_message(chat_id, answer)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling(interval=0, timeout=20)