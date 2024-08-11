import os

from dotenv import load_dotenv

from utils.locale import Locale


load_dotenv()


LOCALE = Locale("ru")

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

DB_FILE = "db.sqlite3"