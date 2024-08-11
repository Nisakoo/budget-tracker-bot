from functools import lru_cache

from telegram import ReplyKeyboardMarkup

from config import LOCALE


@lru_cache
def choose_category_keyboard(categories: tuple) -> ReplyKeyboardMarkup:
    categories = list(categories)
    _keyboard = list()

    if categories:
        for i in range(0, min(len(categories), 9), 3):
            _keyboard.append(categories[i:i+3])

        if not LOCALE["other"] in categories:
            if len(_keyboard[-1]) < 3:
                _keyboard[-1].append(LOCALE["other"])
            else:
                _keyboard.append([LOCALE["other"]])
    else:
        _keyboard.append([LOCALE["other"]])

    _keyboard.append([LOCALE["cancel"]])

    return ReplyKeyboardMarkup(
        _keyboard, resize_keyboard=True
    )

# Maybe make this menu is InlineKeyboard
main_menu = ReplyKeyboardMarkup([
    [LOCALE["incomes"]],
    [LOCALE["expenses"]],
    [LOCALE["export"]],
], resize_keyboard=True)

cancel_button = ReplyKeyboardMarkup([
    [LOCALE["cancel"]]
], resize_keyboard=True)

export_menu = ReplyKeyboardMarkup([
    [LOCALE["incomes"]],
    [LOCALE["expenses"]],
    [LOCALE["cancel"]]
], resize_keyboard=True)

period_menu = ReplyKeyboardMarkup([
    [LOCALE["day_period"], LOCALE["week_period"], LOCALE["month_period"]],
    [LOCALE["csv_option"]],
    [LOCALE["cancel"]]
], resize_keyboard=True)