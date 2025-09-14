# bot/helpers/defend.py
import functools
from aiogram.types import Message
from pyrogram.enums import ChatMemberStatus
from bot import SmartPyro, bot
from bot.helpers.logger import LOGGER
from config import LOG_CHANNEL_ID

def SmartDefender(func):
    @functools.wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        user = message.from_user
        if not user:
            return
        
        try:
            bot_member = await SmartPyro.get_chat_member(LOG_CHANNEL_ID, "me")
            if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await message.reply("The bot needs to be an admin in the log channel to function.")
                return

            await func(message, *args, **kwargs)
        except Exception as e:
            LOGGER.error(f"Error in SmartDefender for user {user.id}: {e}")
    return wrapper