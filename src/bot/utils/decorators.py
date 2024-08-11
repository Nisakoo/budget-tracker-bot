from typing import Any, Callable

from telegram import Update
from telegram.ext import ContextTypes


def database(func) -> Callable:
    """
    Passes database stored in context as argument.
    Used for easy access to database.
    """

    async def inner(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs) -> Any:
        return await func(
            update, context,
            *args, **kwargs,
            db=context.bot_data["db"]
        )

    return inner

def delete_previous_message(func) -> Callable:
    """
    Delete previous bot message.
    """

    async def inner(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs) -> Any:
        if "previous_message_id" in context.user_data:
            if not context.user_data["message_deleted"]:
                await context.bot.delete_message(
                    update.effective_chat.id,
                    context.user_data["previous_message_id"]
                )
                context.user_data["message_deleted"] = True

        return await func(
            update, context,
            *args, **kwargs
        )
    
    return inner