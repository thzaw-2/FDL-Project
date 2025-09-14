import traceback
import sys
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import Message
from bot.helpers.logger import LOGGER
from config import LOG_CHANNEL_ID

async def Smart_Notify(bot: Bot, command: str, e: Exception, message: Message = None):
    try:
        error_traceback = traceback.format_exc()
        if not error_traceback:
            error_traceback = "No traceback available."
        
        error_message = (
            f"**SmartUtilBot Error Notification**\n\n"
            f"**Command:** {command}\n\n"
            f"**Error Details:**\n"
            f"```python\n{e}\n```\n\n"
            f"**Traceback:**\n"
            f"```python\n{error_traceback}\n```"
        )
        
        if message:
            error_message += f"\n\n**User ID:** `{message.from_user.id}`"
            error_message += f"\n**Chat ID:** `{message.chat.id}`"
            error_message += f"\n**Message ID:** `{message.message_id}`"

        await bot.send_message(
            chat_id=LOG_CHANNEL_ID,
            text=error_message,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as notify_e:
        LOGGER.error(f"Failed to send error notification: {notify_e}")
