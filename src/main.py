import logging

import config
from db.sqlite_db import SqliteDB
from bot import telegram_bot


logging.basicConfig(level=logging.INFO)


def main() -> None:
    with SqliteDB(config.DB_FILE) as db:
        telegram_bot.run(config.TOKEN, db)


if __name__ == "__main__":
    main()