from telegram.ext import Application, CommandHandler, MessageHandler, filters

from db.base_database import BaseDataBase
import bot.handlers as handlers


def run(token: str, db: BaseDataBase) -> None:
    app = Application.builder().token(token).build()

    # Set context
    app.bot_data["db"] = db

    # Handlers
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(
        MessageHandler(
            filters.Regex(r"^([а-яА-Я0-9]+) (\+|-)(\d+[,]?\d+?)$"),
            handlers.fast_add
        )
    )
    # export_conv and tracker_conv use the same locales,
    # so there may be a conflict.
    # Since for tracker_conv they are entry_point,
    # and for export_conv they are part of the state.
    # Then they should be in this order
    app.add_handler(handlers.export_conv_handler)
    app.add_handler(handlers.tracker_conv_handler)

    app.run_polling()
