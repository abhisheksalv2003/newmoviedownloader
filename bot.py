from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello World!')

def main() -> None:
    try:
        updater = Updater("6197603731:AAFjEJ2h3TLjoVqUihD2PwGL75LJVq5ypcM", use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        updater.start_polling()
        updater.idle()
        print("Bot successfully deployed")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    main()
  
