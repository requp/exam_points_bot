import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv("TOKEN")

DB_EXAM_TABLE: str = os.getenv('DB_EXAM_TABLE')
DB_USER_TABLE: str = os.getenv("DB_USER_TABLE")
DB_DATA: str = os.getenv("DB_DATA")
