from flask import Flask
from telegram.ext import Updater, MessageHandler, Filters
import discord
import asyncio
import threading
import os

from dotenv import load_dotenv
load_dotenv()

# Получаем токены и ID из переменных окружения
TG_TOKEN = os.getenv("TG_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
PORT = int(os.environ.get("PORT", 10000))

# Flask приложение
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# Настройка Discord intents
intents = discord.Intents.default()
intents.messages = True
discord_client = discord.Client(intents=intents)

# Telegram-бот функция
def run_tg_bot():
    updater = Updater(TG_TOKEN, use_context=True, drop_pending_updates=True)

    def tg_handler(update, context):
        if update.message and update.message.text:
            text = update.message.text
            asyncio.run_coroutine_threadsafe(
                send_to_discord(text), discord_client.loop
            )

    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), tg_handler)
    )

    updater.start_polling()
    updater.idle()

# Отправка сообщения в Discord
async def send_to_discord(message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

# При готовности Discord-бота — запускаем Telegram-бот в отдельном потоке
@discord_client.event
async def on_ready():
    print(f"Discord bot logged in as {discord_client.user}")
    threading.Thread(target=run_tg_bot).start()

# Запуск всего приложения
if __name__ == "__main__":
    # Запускаем Discord-бота в отдельном потоке
    def start_discord():
        discord_client.run(DISCORD_TOKEN)

    threading.Thread(target=start_discord).start()

    # Flask сервер
    app.run(host="0.0.0.0", port=PORT)
