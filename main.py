# main.py
import json
import logging
import os
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, InlineQueryHandler, CallbackContext, CallbackQueryHandler
import asyncio
from telethon import TelegramClient
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
CHANNEL_USERNAMES = os.getenv('CHANNEL_USERNAMES', '').split(',')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Telethon client
telethon_client = TelegramClient('data/session', API_ID, API_HASH)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Load file data
def load_file_data():
    try:
        with open('data/file_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

file_data = load_file_data()

# Load user data
def load_user_data():
    try:
        with open('data/user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

user_data = load_user_data()

def save_user_data():
    with open('data/user_data.json', 'w') as f:
        json.dump(user_data, f)

def get_user_data(user_id: str) -> dict:
    if user_id not in user_data:
        user_data[user_id] = {'joined_channel': False}
        save_user_data()
    return user_data[user_id]

def replace_usernames(text):
    if not text:
        return text
    return re.sub(r'@\w+', CHANNEL_USERNAME, text)

async def scrape_and_update_channel():
    global file_data
    new_file_data = []

    try:
        await telethon_client.start(phone=PHONE_NUMBER)
        logger.info("Telethon Client Created")

        for channel_username in CHANNEL_USERNAMES:
            if not channel_username:
                continue
                
            try:
                channel = await telethon_client.get_entity(channel_username)

                async for message in telethon_client.iter_messages(channel):
                    if message.file:
                        original_caption = message.text if message.text else "No caption"
                        modified_caption = replace_usernames(original_caption)
                        
                        if original_caption != modified_caption:
                            try:
                                await telethon_client.edit_message(channel, message.id, text=modified_caption)
                                logger.info(f"Updated caption for message {message.id}")
                            except Exception as e:
                                logger.error(f"Failed to update caption for message {message.id}: {str(e)}")

                        file_name = message.file.name if message.file.name else "Unnamed file"
                        file_type = message.file.mime_type if message.file.mime_type else "Unknown type"
                        link = f'https://t.me/{channel_username}/{message.id}'
                        new_file_data.append({
                            'file_name': file_name,
                            'file_type': file_type,
                            'caption': modified_caption,
                            'link': f'{link} {CHANNEL_USERNAME}'
                        })
            except Exception as e:
                logger.error(f"Error processing channel {channel_username}: {str(e)}")

        file_data = new_file_data
        with open('data/file_data.json', 'w', encoding='utf-8') as f:
            json.dump(file_data, f, ensure_ascii=False, indent=4)

        logger.info("File data has been updated and saved to file_data.json")
    except Exception as e:
        logger.error(f"Error in scrape_and_update_channel: {str(e)}")
    finally:
        await telethon_client.disconnect()

# [Rest of your existing functions remain the same, just ensure proper error handling]

async def main():
    try:
        # Initialize the application
        application = Application.builder().token(TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("search", search))
        application.add_handler(CommandHandler("broadcast", broadcast))
        application.add_handler(CommandHandler("stats", stats))
        application.add_handler(CommandHandler("refresh", refresh_data))
        application.add_handler(CallbackQueryHandler(refresh, pattern="^refresh$"))
        application.add_handler(InlineQueryHandler(inline_search))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Run the initial scrape and update
        await scrape_and_update_channel()

        # Start the bot
        await application.run_polling()
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())
