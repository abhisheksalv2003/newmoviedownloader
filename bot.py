from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

TOKEN = os.environ.get("6197603731:AAFjEJ2h3TLjoVqUihD2PwGL75LJVq5ypcM")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def register_handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    register_handlers(dispatcher)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
