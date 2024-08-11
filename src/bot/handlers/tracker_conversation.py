from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from config import LOCALE
from bot.utils import decorators
from bot.utils import keyboards
from db.base_database import BaseDataBase
from .commands import *


CHOOSE_CATEGORY, SET_AMOUNT = 0, 1


@decorators.database
@decorators.whitelist
async def tracker_start(
        update: Update, context: ContextTypes.DEFAULT_TYPE, db: BaseDataBase) -> int:
    # I know that I can write it in one row
    # but it wouldn't be readable
    if update.effective_message.text == LOCALE["incomes"]:
        context.user_data["is_income"] = True
    else:
        context.user_data["is_income"] = False

    categories = await db.get_categories(
        update.effective_user.id,
        context.user_data["is_income"]
    )

    await update.effective_message.reply_text(
        LOCALE["choose_category"],
        reply_markup=keyboards.choose_category_keyboard(tuple(categories))
    )

    return CHOOSE_CATEGORY


async def tracker_choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["category"] = update.effective_message.text.strip()

    await update.effective_message.reply_text(
        LOCALE["set_amount"],
        reply_markup=keyboards.cancel_button
    )

    return SET_AMOUNT


@decorators.database
async def tracker_set_amount(
        update: Update, context: ContextTypes.DEFAULT_TYPE, db: BaseDataBase) -> int:
    amount = update.effective_message.text.strip()
    amount = amount.replace(",", ".")
    amount = amount.replace(" ", "")

    try:
        # Simple validator
        amount = float(amount)
    except:
        await update.effective_message.reply_text(
            LOCALE["incorrect_amount"],
            reply_markup=keyboards.cancel_button
        )
        return SET_AMOUNT

    await db.add(
        update.effective_user.id,
        context.user_data["is_income"],
        context.user_data["category"],
        amount
    )
        
    await update.effective_message.reply_text(
        LOCALE["done"],
        reply_markup=keyboards.main_menu
    )

    return ConversationHandler.END


tracker_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Text([
                    LOCALE["incomes"],
                    LOCALE["expenses"]
                ]), tracker_start),
    ],
    states={
        CHOOSE_CATEGORY: [
            MessageHandler(
                ~filters.Text([
                    LOCALE["cancel"]
                ]), tracker_choose_category)
        ],
        SET_AMOUNT: [
            MessageHandler(
                ~filters.Text([
                    LOCALE["cancel"]
                ]), tracker_set_amount)
        ]
    },
    fallbacks=[
        MessageHandler(
            filters.Text([
                LOCALE["cancel"]
            ]), end_conversation)
    ]
)