import re

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from config import LOCALE
from bot.utils import keyboards, decorators
from db.base_database import BaseDataBase


# TODO: add /delete /head
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Start command handler.
    Just send hello message.
    """
    await update.effective_message.reply_text(
        LOCALE.format("start_message", name=update.effective_user.name),
        reply_markup=keyboards.main_menu
    )


async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ends current conversation.
    """
    await start(update, context)
    return ConversationHandler.END


@decorators.database
@decorators.whitelist
async def fast_add(
        update: Update, context: ContextTypes.DEFAULT_TYPE, db: BaseDataBase) -> None:
    """
    Command for adding incomes and expenses.
    Syntax: ^([а-яА-Я0-9]+) (\+|-)(\d+[,]?\d+?)$
    """
    message = update.effective_message.text
    values = re.findall(r"^([а-яА-Я0-9]+) (\+|-)(\d+[,]?\d+?)$", message)[0]

    category = values[0]
    is_income = (values[1] == "+")
    amount = float(values[2].replace(",", "."))

    await db.add(
        update.effective_user.id,
        is_income,
        category,
        amount
    )

    await update.effective_message.reply_text(
        LOCALE["done"],
        reply_markup=keyboards.main_menu
    )