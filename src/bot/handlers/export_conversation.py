from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from telegram.constants import ParseMode

from config import LOCALE
from bot.utils import *
from .commands import *
from db.base_database import BaseDataBase, Period
from utils.functions import get_csv, get_image


CHOOSE_CATEGORY, SET_PERIOD = 0, 1


async def export_start(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.reply_text(
        LOCALE["export_start"],
        reply_markup=keyboards.export_menu
    )

    return CHOOSE_CATEGORY


async def export_choose_category(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # I know that I can write it in one row
    # but it wouldn't be readable
    if update.effective_message.text == LOCALE["incomes"]:
        context.user_data["is_income"] = True
    else:
        context.user_data["is_income"] = False

    await update.effective_message.reply_text(
        LOCALE["export_set_period"],
        reply_markup=keyboards.period_menu
    )

    return SET_PERIOD


@decorators.database
async def export_set_period(
        update: Update, context: ContextTypes.DEFAULT_TYPE, db: BaseDataBase) -> None:
    period_text = update.effective_message.text.strip()

    if period_text == LOCALE["day_period"]:
        period = Period.DAY
    elif period_text == LOCALE["week_period"]:
        period = Period.WEEK
    elif period_text == LOCALE["month_period"]:
        period = Period.MONTH
    elif period_text == LOCALE["csv_option"]:
        period = Period.ALLTIME

    data = await db.fetch(
        update.effective_user.id,
        context.user_data["is_income"],
        period
    )

    if period == Period.ALLTIME:
        with get_csv(data) as file:
            await update.effective_message.reply_document(
                file,
                reply_markup=keyboards.main_menu
            )
    else:
        if data:
            sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
            total_amount = sum(i[1] for i in sorted_data)

            message = str()
            for i in sorted_data:
                message += f"<b>{i[0]}</b> {i[1]:.2f}{LOCALE['currency']} ({i[1]/total_amount:.2%})\n"

            await update.effective_message.reply_text(
                message, reply_markup=keyboards.main_menu,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.effective_message.reply_text(
                LOCALE["no_data"], reply_markup=keyboards.main_menu,
            )
        # Not as good as I want it to be.
        # with get_image(data, context.user_data["is_income"], period) as img:
        #     await update.effective_message.reply_photo(
        #         img,
        #         reply_markup=keyboards.main_menu
        #     )

    return ConversationHandler.END


export_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Text([
                LOCALE["export"]
            ]), export_start)
    ],
    states={
        CHOOSE_CATEGORY: [
            MessageHandler(
                filters.Text([
                    LOCALE["incomes"],
                    LOCALE["expenses"]
                ]), export_choose_category),
        ],
        SET_PERIOD: [
            MessageHandler(
                filters.Text([
                    LOCALE["day_period"],
                    LOCALE["week_period"],
                    LOCALE["month_period"],
                    LOCALE["csv_option"]
                ]), export_set_period)
        ]
    },
    fallbacks=[
        MessageHandler(
            filters.Text([
                LOCALE["cancel"]
            ]), end_conversation)
    ]
)