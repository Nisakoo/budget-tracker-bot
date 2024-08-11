## About
This is a Telegram bot that simplifies the process of managing personal income and expenses.

The bot is not designed for analysis, so I recommend exporting the data and analyzing it in another program.

Bot Commands:
- **/start** - displays an information message and the main menu.
- **Quick adding**: allows you to quickly enter data, has the following format
```
[category] [+ or -][amount]
```
The main menu contains three tabs: income, expenses and export.

The first two tabs allow you to enter data, and the third one allows you to export data.

You can view income and expenses for a certain period (day, week, month) directly in the bottom.

For a more complex analysis, you should select `CSV` in the export menu.

## Setup
1. Create `.env` (see [example.env](example.env)) file and specify the following variables:
    - `TOKEN` - Telegram bot token.
    - `ADMIN_ID` - Your Telegram user ID.
    - `LOCALE_FILE` - File path with localizations.
    - `DB_FILE` - Database file (for sqlite3).
2. Run
```
docker-compose up --build
```
