import os

from dotenv import load_dotenv

from utils.locale import Locale


load_dotenv()


TOKEN = os.getenv("TOKEN")
LOCALE = Locale("ru")

DB_FILE = "db.sqlite3"