from telegram import Update
from telegram.ext import ContextTypes


async def send_message(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs) -> None:
    posted_message = await update.effective_message.reply_text(
        *args, **kwargs
    )

    context.user_data["previous_message_id"] = posted_message.id
    context.user_data["message_deleted"] = False