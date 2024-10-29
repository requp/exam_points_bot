import psycopg2
from psycopg2 import Error
from settings import DB_DATA, DB_USER_TABLE


def connect_to_db() -> tuple | None:
    try:
        connection = psycopg2.connect(DB_DATA)
        cursor = connection.cursor()
        return connection, cursor
    except (Exception, Error) as error:
        error = f"Ошибка при работе с PostgreSQL {error}"
        print(error)


def save_exam_score_query(user_id: int, exam_score: int) -> bool:
    res: bool = False
    try:
        connection = psycopg2.connect(DB_DATA)
        cursor = connection.cursor()
        query: str = f"\
        UPDATE {DB_USER_TABLE} \
        SET score={exam_score} \
        WHERE telegram_user_id = {user_id};"
        cursor.execute(query)
        connection.commit()
        return True
    except (Exception, Error) as error:
        error = f"Ошибка при работе с PostgreSQL {error}"
        print(error)
    return res


def save_user_data_query(user_id: int, first_name: str, last_name: str):
    connection, cursor = connect_to_db()
    query: str = f"\
    INSERT INTO {DB_USER_TABLE} (telegram_user_id, first_name, last_name) \
    VALUES ({user_id}, '{first_name}', '{last_name}');"
    cursor.execute(query)
    connection.commit()


def get_user_query(user_id: int, requested_fields: str) -> tuple:
    connection, cursor = connect_to_db()
    query: str = f"\
    SELECT {requested_fields} \
    FROM {DB_USER_TABLE} \
    WHERE telegram_user_id = {user_id};"
    cursor.execute(query)
    return cursor.fetchone()
