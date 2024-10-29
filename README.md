Описание установки:
установить окружение venv с Python 3.11
включить окружение
установить все пакеты из requirements: pip install requirements.txt
установить docker
создать директории db/backup, db/data
запустить докер контейнер: docker-compose up -d db
создать таблицу, поменять root на собственного юзера:

CREATE TABLE public."user" (
    id serial PRIMARY KEY,
    telegram_user_id bigint NOT NULL,
    first_name VARCHAR(255) varying,
    last_name VARCHAR(255) varying,
    score integer,
);

ALTER TABLE public."user" OWNER TO root;

запустить программу через файл main.py