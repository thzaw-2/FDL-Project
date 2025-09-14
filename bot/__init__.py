# File path: bot/__init__.py
import os
from pyrogram import Client
from aiogram import Bot, Dispatcher

# Initialize Pyrogram Client
try:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    SmartPyro = Client(
        "SmartUtilBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        parse_mode="html",
        sleep_threshold=3600
    )
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
except Exception as e:
    # Handle initialization error
    pass
