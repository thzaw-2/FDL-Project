import asyncio
import os
from aiogram import Bot, Dispatcher
from pyrogram import Client
from bot.helpers.logger import LOGGER
import fdl
import status

LOGGER.info("Starting bot...")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

try:
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
    dp.include_router(fdl.router)
    dp.include_router(status.router)
except Exception as e:
    LOGGER.error(f"Error initializing bot: {e}")
    exit(1)

async def main():
    try:
        await SmartPyro.start()
        await dp.start_polling(bot)
    except Exception as e:
        LOGGER.error(f"Error in main polling loop: {e}")
    finally:
        await SmartPyro.stop()

if __name__ == "__main__":
    asyncio.run(main())
