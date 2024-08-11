import os

from dotenv import load_dotenv

from utils.locale import Locale


load_dotenv()


TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
LOCALE_FILE = os.getenv("LOCALE_FILE")
DB_FILE = os.getenv("DB_FILE")

LOCALE = Locale("ru", LOCALE_FILE)