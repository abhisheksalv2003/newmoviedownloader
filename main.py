import json
from telegram import Update,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,InlineQueryHandler


# File to store the captions and links
DATA_FILE = 'data.json'

def load_data() -> dict:
    """Load data from the file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data: dict) -> None:
    """Save data to the file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Load the captions and links from the file
CAPTIONS_LINKS = load_data()

def add(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) == 2:
        caption, link = args
        if caption in CAPTIONS_LINKS:
            update.message.reply_text(f'The caption "{caption}" already exists.')
        else:
            CAPTIONS_LINKS[caption] = link
            save_data(CAPTIONS_LINKS)  # Save the updated data
            update.message.reply_text(f'Added "{caption}" with link "{link}"')
    else:
        update.message.reply_text('Usage: /add caption link')
# Function to handle the /remove command
def remove(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id  # Get the user id of the sender
    if user_id == 5460878369:  # Replace ADMIN_USER_ID with the actual admin user id
        args = context.args
        if len(args) == 1:
            caption = args[0]
            if caption in CAPTIONS_LINKS:
                del CAPTIONS_LINKS[caption] 
                save_data(CAPTIONS_LINKS) # Save the updated data 
                update.message.reply_text(f'Removed "{caption}" from the data.')
            else:
                update.message.reply_text(f'The caption "{caption}" does not exist in the data.')
        else:
            update.message.reply_text('Usage: /remove caption')
    else:
        update.message.reply_text('You are not authorized to use this command.')

def notes(update: Update, context: CallbackContext) -> None:
    """Display all the added captions and links."""
    if CAPTIONS_LINKS:
        notes = '\n'.join(f'{caption}: {link}' for caption, link in CAPTIONS_LINKS.items())
        update.message.reply_text(notes)
    else:
        update.message.reply_text('No notes added yet.')

def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    for caption, link in CAPTIONS_LINKS.items():
        if caption in message_text:
            update.message.reply_text(link)
            break

# Define the /request command handler
def request(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text

    # Forward the user's message to the admin
    admin_chat_id = 5460878369
    context.bot.send_message(admin_chat_id, f"User {user_id} has made a request: {user_message}")
#def save_user_id(update: Update, context: CallbackContext) -> None:
 #   user_id = update.message.from_user.id
  #  with open(f'{user_id}_name.txt', 'w') as f:
        # Your code here
"""class BotStatis tics:
         def init(self):
        self.active_ users = set()
        self.banned_users = set()

    def get_active_users_count(self):
        return len(self.active_users)

    def get_banned_users_count(self):
        return len(self.banned_users)

    def ban_user(self, user_id):
        self.banned_users.add(user_id)
        if user_id in self.active_users:
            self.active_users.remove(user_id)

    def unban_user(self, user_id):
        if user_id in self.banned_users:
            self.banned_users.remove(user_id)

    def add_active_user(self, user_id):
        self.active_users.add(user_id)

    def remove_active_user(self, user_id):
        if user_id in self.active_users:
            self.active_users.remove(user_id)

# Initialize an instance of the BotStatistics class
bot_stats = BotStatistics()

# Add the /stats command to your Telegram bot code
def stats(update, context):
    active_users_count = bot_stats.get_active_users_count()
    banned_users_count = bot_stats.get_banned_users_count()
    update.message.reply_text(f"Active users: {active_users_count}\nBanned users: {banned_users_count}")

# Add the /ban command to ban a user
def ban_user(update, context):
    user_id = update.message.from_user.id
    bot_stats.ban_user(user_id)
    update.message.reply_text("User has been banned.")

# Add the /unban command to unban a user
def unban_user(update, context):
    user_id = update.message.from_user.id
    bot_stats.unban_user(user_id)
    update.message.reply_text("User has been unbanned.")

# Add the /activeusers command to get the count of active users
def active_users(update, context):
    active_users_count = bot_stats.get_active_users_count()
    update.message.reply_text(f"Active users: {active_users_count}")

# Add the /bannedusers command to get the count of banned users
def banned_users(update, context):
    banned_users_count = bot_stats.get_banned_users_count()
    update.message.reply_text"""
def inline_search(update: Update,context: CallbackContext) -> None:
    query = update.inline_query.query
    results = []

    for caption, link in CAPTIONS_LINKS.items():
        if query.lower() in caption.lower():
            results.append(
                InlineQueryResultArticle(
                    id=caption,
                    title=caption,
                    input_message_content=InputTextMessageContent(link)
                )
            )

    update.inline_query.answer(results)

def main() -> None:
    updater = Updater("6988786922:AAFyJbjpuhV-ZqpzQn0nelMQ72reizwh6EI")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("notes", notes))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
#    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_user_id))
 #   dispatcher.add_handler(CommandHandler("stats", stats))
  #  dispatcher.add_handler(CommandHandler("ban", ban_user))
    #dispatcher.add_handler(CommandHandler("unban", unban_user))
   # dispatcher.add_handler(CommandHandler("activeusers", active_users))
      #ispatcher.add_handler(CommandHandler("bannedusers", banned_users))
    dispatcher.add_handler(CommandHandler("request", request))
    dispatcher.add_handler(InlineQueryHandler(inline_search))
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

