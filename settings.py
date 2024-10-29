import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv("TOKEN")
CHAT_ID: str = os.getenv("CHAT_ID")

DB_USER_TABLE: str = os.getenv("DB_USER_TABLE")
DB_DATA: str = os.getenv("DB_DATA")
