import telegram.ext
from telegram import Update


TOKEN = '6463124467:AAFtqwsJ-yIiM0ZTsEv48l9Pl9XcqDv5JoM'


async def help(update, context):
    await update.message.reply_text("""
    The bot is intended for agricultural people who want to know
    in which region in Israel it is possible to grow different
    plants based on environmental criteria that plants require""")


async def start(update, context):
    await update.message.reply_text("""
    Welcome to Agricultural bot!
    
    The following commands are available:
    
    /start -> This Massage
    /help -> Information on this bot
    """)


async def massege_handler(update, context):
    await update.message.reply_text(update.message.text)


app = telegram.ext.Application.builder().token(TOKEN).build()


app.add_handler(telegram.ext.CommandHandler('start', start))
app.add_handler(telegram.ext.CommandHandler('help', help))
app.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.TEXT, massege_handler))


app.run_polling(poll_interval=2)


