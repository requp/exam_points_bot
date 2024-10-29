import telebot
from telebot.types import Message

from db_logic import save_user_data_query, get_user_query, save_exam_score_query
from settings import TOKEN

MAX_SCORES = 100
MIN_SCORES = 0

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message: Message):
    bot.reply_to(
        message,
        f"Привет, {message.from_user.username}. "
        "Это бот онлайн школы 'Умскул'. Здесь ты можешь зарегестрироваться, "
        "указать свои баллы ЕГЭ и посмотреть их. "
        "Для регистрации введи команду /registr"
    )
    print(message)


@bot.message_handler(commands=['registr'])
def registration(message: Message):
    user_data: None | tuple = get_user_query(
        user_id=message.from_user.id,
        requested_fields="first_name, last_name"
    )
    if isinstance(user_data, tuple):
        first_name, last_name = user_data
        bot.reply_to(
            message,
            f"Ты уже зарестирован под именем {first_name} {last_name}."
        )
    else:
        bot.reply_to(
            message,
            f"Для регистрации введи своё имя и фамилию. "
            "Введи своё имя и фамилию как это указано ниже \nИван Иванов"
        )
        bot.register_next_step_handler(message, handle_registration)


def handle_registration(message: Message):
    if ' ' not in message.any_text or len(message.any_text.split()) != 2:
        bot.reply_to(
            message,
            "Твоё имя и фамилия не содержат пробел или не состоят из 2 слов. "
            "Попробуй ещё раз. Для регистрации введи команду /registr"
        )
    else:
        first_name, last_name = message.any_text.split()
        if not first_name.isalpha() or not last_name.isalpha():
            bot.reply_to(
                message,
                "Твоё имя и/или фамилия содержат в себе не буквенные символы. "
                "Попробуй ещё раз. Для регистрации введи команду /registr"
            )
        else:
            bot.reply_to(
                message,
                f"Добро пожаловать {first_name} {last_name}!"
                "Для того, чтобы ввести свои баллы введи команду /enter_scores"
            )
            save_user_data_query(
                user_id=message.from_user.id, first_name=first_name, last_name=last_name
            )


@bot.message_handler(commands=['enter_scores'])
def enter_scores(message: Message):
    user_data: None | tuple = get_user_query(
        user_id=message.from_user.id,
        requested_fields="id, first_name, last_name, score"
    )
    if user_data is None:
        bot.reply_to(
            message,
            "Ты еще не зарегистрирован. Для регистрации введи /registr"
        )
    else:
        db_user_id, first_name, last_name, score = user_data
        if score:
            bot.reply_to(
                message,
                f"Ты уже ввёл баллы по экзамену. Кол-во баллов: {score}."
            )
        else:
            bot.reply_to(
                message,
                f"Введи число в диапозоне от {MIN_SCORES} до {MAX_SCORES}."
            )
            bot.register_next_step_handler(message, handle_enter_scores)


def handle_enter_scores(message: Message):
    if not message.any_text.isdigit() or not (MIN_SCORES < int(message.any_text) < MAX_SCORES):
        bot.reply_to(
            message,
            f"Ты можешь ввести только целое число в диапозоне от {MIN_SCORES} до {MAX_SCORES}. "
            f"Для ввода баллов введи команду /enter_scores"
        )
    else:
        res: bool = save_exam_score_query(
            user_id=message.from_user.id,
            exam_score=int(message.any_text)
        )
        if res:
            bot.reply_to(
                message,
                f"Баллы сохранены успешно"
            )


@bot.message_handler(commands=['view_scores'])
def view_scores(message: Message):
    user_data: None | tuple = get_user_query(
        user_id=message.from_user.id,
        requested_fields="id, first_name, last_name, score"
    )
    if user_data is None:
        bot.reply_to(
            message,
            "Ты еще не зарегистрирован. Для регистрации введи /registr"
        )
    else:
        db_user_id, first_name, last_name, score = user_data
        if not score:
            bot.reply_to(
                message,
                "Ты ещё не заполнил поле баллов. Для заполнения введи команду /enter_scores"
            )
        else:
            bot.reply_to(
                message,
                f'{first_name} {last_name}, кол-во баллов: {score}'
            )


bot.polling(none_stop=True)
