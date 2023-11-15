import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardButton

# Replace with your Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create the Telegram bot updater
updater = Updater(BOT_TOKEN)

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Welcome to my custom Telegram bot!',
                             reply_markup=ReplyKeyboardMarkup([[ReplyKeyboardButton('Help')]]))

# Define a function to handle the /help command
def help(update, context):
    update.message.reply_text('Available commands:\n/start - Starts the bot\n/help - Displays this help message')

# Define a function to handle all incoming messages
def message(update, context):
    if update.message.text.lower() == 'help':
        help(update, context)
    else:
        update.message.reply_text(f'You sent me: {update.message.text}')

# Register the /start and /help handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message))

# Set the webhook URL
updater.dispatcher.bot.set_webhook(os.getenv("WEBHOOK_URL"))

# Start the bot
updater.start_webhook(port=os.getenv("PORT"), listen='0.0.0.0')

# Check for updates
updater.idle()
