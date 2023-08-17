import telegram.ext
from telegram import Update
from main_app import message_handler

TOKEN = '6463124467:AAFtqwsJ-yIiM0ZTsEv48l9Pl9XcqDv5JoM'


# Command handler for the /help command
async def help(update, context):
    await update.message.reply_text("""
    The bot is intended for agricultural people who want to know
    in which region in Israel it is possible to grow different
    plants based on environmental criteria that plants require""")


# Command handler for the /start command
async def start(update, context):
    await update.message.reply_text("""
    Welcome to Agricultural bot!

    The following commands are available:

    /start -> This Message
    /help -> Information on this bot
    """)


# Handler for any text message
async def message_handler(update, context):
    user_id = str(update.message.from_user.id)
    response = await message_handler(update.message.text, user_id)
    await update.message.reply_text(response)


# Run the server on an available port
if __name__ == '__main__':
    # Build the bot application
    app = telegram.ext.Application.builder().token(TOKEN).build()

    # Add command and message handlers
    app.add_handler(telegram.ext.CommandHandler('start', start))
    app.add_handler(telegram.ext.CommandHandler('help', help))
    app.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.TEXT, message_handler))

    # Run the bot application with polling
    app.run_polling(poll_interval=2)


