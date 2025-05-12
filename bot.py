from telegram.ext import Updater, MessageHandler, Filters
import discord
import asyncio
import os
from dotenv import load_dotenv
from flask import Flask

# Загружаем переменные из .env
load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Flask-приложение для Render
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

# Настройка Discord-клиента с интентами
intents = discord.Intents.default()
intents.messages = True
discord_client = discord.Client(intents=intents)

# Функция запуска Telegram-бота
def start_tg_bot():
    updater = Updater(TG_TOKEN, use_context=True)

    def tg_handler(update, context):
        if update.message and update.message.text:
            text = update.message.text
            asyncio.run_coroutine_threadsafe(
                send_to_discord(text), discord_client.loop
            )

    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), tg_handler))
    updater.start_polling()

# Отправка сообщений в Discord
async def send_to_discord(message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

# Событие запуска Discord-бота
@discord_client.event
async def on_ready():
    print(f'Discord bot logged in as {discord_client.user}')
    start_tg_bot()

# Запуск Discord-бота
if __name__ == "__main__":
    discord_client.run(DISCORD_TOKEN)
