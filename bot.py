from telegram.ext import Updater, MessageHandler, Filters
import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("5462407742:AAEdJ33X9sjEplXkB02MmQ7Trio-erDgYCk")
DISCORD_TOKEN = os.getenv("7ceb4b62f30e862fbc3f24d51dbab0aaa0a006c8045a28b758afd0a19af43a31")
DISCORD_CHANNEL_ID = int(os.getenv("539051035512274954"))

discord_client = discord.Client()

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

async def send_to_discord(message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

@discord_client.event
async def on_ready():
    print(f'Discord bot logged in as {discord_client.user}')
    start_tg_bot()

discord_client.run(DISCORD_TOKEN)