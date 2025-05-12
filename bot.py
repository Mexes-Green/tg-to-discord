from flask import Flask
from threading import Thread
from telegram.ext import Updater, MessageHandler, Filters
import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Получение токенов и ID из .env
TG_TOKEN = os.getenv("TG_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Flask-приложение (для Render, просто заглушка)
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

# Настройка Discord Intents
intents = discord.Intents.default()
intents.messages = True
discord_client = discord.Client(intents=intents)

# Telegram-бот запускается в отдельном потоке
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
    updater.idle()

# Отправка сообщений в Discord
async def send_to_discord(message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

@discord_client.event
async def on_ready():
    print(f'[Discord] Logged in as {discord_client.user}')
    Thread(target=start_tg_bot).start()

# Запуск Flask + Discord клиента
if __name__ == '__main__':
    Thread(target=lambda: discord_client.run(DISCORD_TOKEN)).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
