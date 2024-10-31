import logging
from datetime import datetime

import psycopg2
from psycopg2 import Error
from settings import DB_DATA, DB_USER_TABLE, DB_EXAM_TABLE


def connect_to_db_and_execute_query(
        query: str,
        commit_flag: bool = False,
) -> tuple:
    """Позволяет подключится к БД и исполнить запрос"""
    data: list = []
    try:
        connection = psycopg2.connect(DB_DATA)
        cursor = connection.cursor()
        cursor.execute(query)
        if commit_flag:
            connection.commit()
        else:
            data = cursor.fetchall()
        return True, data
    except (Exception, Error) as error:
        error = f"Ошибка при работе с PostgreSQL {error} -- {datetime.now()}"
        logging.error(error)
        return False, data


def save_exam_score_query(user_id: int, exam_name: str, exam_score: int) -> bool:
    """Сохраняет баллы по конкретному предмету"""
    query: str = f"\
            INSERT INTO {DB_EXAM_TABLE} (name, score, user_id)\
            VALUES ('{exam_name}', {exam_score}, {user_id});"
    return connect_to_db_and_execute_query(
        query=query, commit_flag=True
    )[0]


def save_user_data_query(user_id: int, first_name: str, last_name: str) -> bool:
    """Регистрирует пользователся в БД"""
    query: str = f"\
        INSERT INTO {DB_USER_TABLE} (telegram_user_id, first_name, last_name) \
        VALUES ({user_id}, '{first_name}', '{last_name}');"
    return connect_to_db_and_execute_query(
        query=query, commit_flag=True
    )[0]


def get_user_query(
        user_id: int,
        requested_fields: str = "id, first_name, last_name"
) -> tuple:
    """Получает данные баллов пользователя по экзаменам"""
    query: str = f"\
        SELECT {requested_fields} \
        FROM {DB_USER_TABLE} \
        WHERE telegram_user_id = {user_id} LIMIT 1;"
    res_flag, user_data = connect_to_db_and_execute_query(
        query=query
    )
    return res_flag, user_data


def get_exam_scores_query(
        user_id: int,
        requested_fields: str = "name, score"
) -> tuple:
    """Возвращает данные пользователя по всем предметам баллы к которым он ввёл"""
    query: str = f"\
    SELECT {requested_fields} \
    FROM {DB_EXAM_TABLE} \
    WHERE user_id = {user_id};"
    return connect_to_db_and_execute_query(
        query=query
    )

def user_is_registered(user_id: int) -> bool:
    """Проверяет, зарегистрирован ли пользователь"""
    res_flag, user_data = get_user_query(user_id)
    return res_flag and bool(user_data)

def get_user_name(user_id: int) -> tuple:
    """Возвращает имя и фамилию пользователя"""
    res_flag, user_data = get_user_query(user_id, requested_fields="first_name, last_name")
    return res_flag, user_data[0] if res_flag else None

def score_exists(user_id: int, exam_name: str) -> bool:
    """Проверяет, есть ли уже введённый ранее балл по указанному предмету"""
    res_flag, user_exams = get_exam_scores_query(user_id)
    if res_flag:
        for exam in user_exams:
            if exam[0] == exam_name:
                return True
    return False
