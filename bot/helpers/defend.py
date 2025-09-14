import functools
from aiogram.types import Message
from pyrogram.enums import ChatMemberStatus
from bot import SmartPyro
from bot.helpers.logger import LOGGER
from bot.helpers.botutils import send_message
from config import LOG_CHANNEL_ID, BOT_STATUS, ADMINS

def SmartDefender(func):
    @functools.wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        user = message.from_user
        if not user:
            return

        if BOT_STATUS == "off" and user.id not in ADMINS:
            await send_message(
                chat_id=message.chat.id,
                text="<b>Sorry, the bot is currently in maintenance mode.</b>",
                parse_mode=ParseMode.HTML
            )
            return

        try:
            bot_member = await SmartPyro.get_chat_member(LOG_CHANNEL_ID, "me")
            if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await send_message(
                    chat_id=message.chat.id,
                    text="<b>The bot needs to be an admin in the log channel to function.</b>",
                    parse_mode=ParseMode.HTML
                )
                return

            await func(message, *args, **kwargs)
        except Exception as e:
            LOGGER.error(f"Error in SmartDefender for user {user.id}: {e}")
    return wrapper
