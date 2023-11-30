import telegram
import os

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

bot = (link unavailable)(TOKEN)

@bot.command(name='start')
async def start(update, context):
print(f'Start command received from {update.effective_user.username}')

bot.start_polling()
