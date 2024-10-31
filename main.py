import telebot
from telebot.types import Message

from constant_variables import MIN_SCORES, MAX_SCORES, EXAM_NAMES
from db_logic import (
    save_user_data_query,
    get_user_query,
    save_exam_score_query,
    get_exam_scores_query,
    user_is_registered,
    get_user_name,
    score_exists
)
from settings import TOKEN


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


@bot.message_handler(commands=['registr'])
def registration(message: Message):
    if user_is_registered(message.from_user.id):
        db_user_id, first_name, last_name = get_user_name(message.from_user.id)
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
    if len(message.text.split()) != 2:
        bot.reply_to(
            message,
            "Твоё имя и фамилия не содержат пробел или не состоят из 2 слов. "
            "Попробуй ещё раз. Для регистрации введи команду /registr"
        )
    else:
        first_name, last_name = message.text.split()
        if not first_name.isalpha() or not last_name.isalpha():
            bot.reply_to(
                message,
                "Твоё имя и/или фамилия содержат в себе не буквенные символы. "
                "Попробуй ещё раз. Для регистрации введи команду /registr"
            )
        else:
            res_flag = save_user_data_query(
                user_id=message.from_user.id, first_name=first_name, last_name=last_name
            )
            if res_flag:
                bot.reply_to(
                    message,
                    f"Добро пожаловать {first_name} {last_name}!"
                    "Для того, чтобы ввести свои баллы введи команду /enter_scores"
                )


@bot.message_handler(commands=['enter_scores'])
def enter_scores(message: Message):
    if user_is_registered(message.from_user.id):
        bot.reply_to(
            message,
            "Ниже приведён список предметов ЕГЭ, которые можно внести:\n"
            f"{', '.join(EXAM_NAMES)}.\n"
            "Напиши название экзамена и кол-во баллов как показано в примере:\n"
            "Русский язык 90"
        )
        bot.register_next_step_handler(message, handle_enter_scores)
    else:
        bot.reply_to(
            message,
            "Ты еще не зарегистрирован. Для регистрации введи /registr"
        )


def handle_enter_scores(message: Message):
    exam_info: list = message.text.split()
    if not (2 <= len(exam_info) <= 3):
        bot.reply_to(
            message,
            f"Текст должен состоять из названия предмета и числа баллов. "
            f"Для ввода баллов введи команду /enter_scores"
        )
    else:
        # Проверяем строку на наличие предмета из 2 слов (напр. русский язык)
        if len(exam_info) == 3:
            exam_name, exam_score = f"{exam_info[0]} {exam_info[1]}", exam_info[2]
        else:
            exam_name, exam_score = exam_info

        if not exam_score.isdigit():
            bot.reply_to(
                message,
                f"Текст должен состоять из названия предмета и числа баллов. "
                f"Для ввода баллов введи команду /enter_scores"
            )
        else:
            exam_score = int(exam_score)
            if not (MIN_SCORES <= exam_score <= MAX_SCORES):
                bot.reply_to(
                    message,
                    f"Ты можешь ввести только целое число в диапозоне от {MIN_SCORES} до {MAX_SCORES}. "
                    f"Для ввода баллов введи команду /enter_scores"
                )
            elif exam_name.lower() not in [exam.lower() for exam in EXAM_NAMES]:
                bot.reply_to(
                    message,
                    f"Введённое тобой название не входит в список предметов. "
                    f"Для ввода баллов введи команду /enter_scores"
                )
            else:
                res_flag, user_data = get_user_query(user_id=message.from_user.id)
                if res_flag and user_data:
                    db_user_id = user_data[0][0]
                    if score_exists(db_user_id, exam_name):
                        bot.reply_to(
                            message,
                            "Ты уже ввёл баллы по этому предмету. Введи другой предмет."
                        )
                    else:
                        res_flag = save_exam_score_query(
                            user_id=db_user_id,
                            exam_name=exam_name,
                            exam_score=exam_score
                        )
                        if res_flag:
                            bot.reply_to(
                                message,
                                f"Баллы успешно сохранены"
                            )
                else:
                    bot.reply_to(
                        message,
                        "Ошибка при получении данных о пользователе. Попробуй ещё раз."
                    )


@bot.message_handler(commands=['view_scores'])
def view_scores(message: Message):
    if user_is_registered(message.from_user.id):
        res_flag, user_data = get_user_query(
            user_id=message.from_user.id,
        )
        if res_flag:
            if not user_data:
                bot.reply_to(
                    message,
                    "Ты ещё не заполнил поле баллов. Для заполнения введи команду /enter_scores"
                )
            else:
                db_user_id, first_name, last_name = user_data[0]
                res_flag, user_exams = get_exam_scores_query(user_id=db_user_id)
                exam_data: dict = dict((name, score) for name, score in user_exams)
                if not exam_data:
                    bot.reply_to(
                        message,
                        "Ты ещё не заполнил поле баллов. Для заполнения введи команду /enter_scores"
                    )
                else:
                    exam_table: str = ''
                    for name, score in exam_data.items():
                        exam_table += f'{name.capitalize()} -- {score}\n'
                    bot.reply_to(
                        message,
                        f"{first_name} {last_name}, твоя таблица заполенных баллов ЕГЭ\n"
                        f"{exam_table}"
                    )
        else:
            bot.reply_to(
                message,
                f"Ошибка при получении данных о пользователе. Попробуйте ещё раз."
            )
    else:
        bot.reply_to(
            message,
            "Ты еще не зарегистрирован. Для регистрации введи /registr"
        )


bot.polling(none_stop=True)
