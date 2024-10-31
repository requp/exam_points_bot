# Exam scores bot

## Описание

Этот Telegram-бот предназначен для управления оценками пользователей.

### Основные функции:

- Регистрация пользователей.
- Оставление баллов по каждому экзамену.
- Получение прописанных баллов ЕГЭ.

## Установка на Linux

Следуйте этим шагам для установки и настройки бота на вашей системе Linux:

#### 1. Установить окружение venv с Python 3.11
#### 2. Включить окружение
#### 3. Установить все пакеты из requirements:
```bash 
pip install requirements.txt
```
#### 4. Создать и заполнить файлы .env и .dockerenv основываясь на их примерах
#### 5. Установить docker
#### 6. Запустить докер контейнер
```bash 
docker-compose up -d db
```
#### 7. Создать 2 таблицы для user и score
```sql
-- Создание таблицы для пользователей
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  telegram_user_id BIGINT NOT NULL UNIQUE,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы для экзаменов
CREATE TABLE score (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
  user_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

```
#### 8. Запустить программу через файл main.py

