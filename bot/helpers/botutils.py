import asyncio
from typing import Union
from aiogram import Bot
from aiogram.types import Message
from pyrogram import Client, types, enums
from bot.helpers.logger import LOGGER

async def send_message(chat_id: Union[int, str], text: str, parse_mode: str = "html", reply_to_message_id: int = None):
    try:
        sent_message = await Bot.get_current().send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_to_message_id=reply_to_message_id
        )
        return sent_message
    except Exception as e:
        LOGGER.error(f"Error sending message: {e}")
        return None

async def delete_messages(chat_id: Union[int, str], message_ids: Union[int, list[int]]):
    if not isinstance(message_ids, list):
        message_ids = [message_ids]
    try:
        await Bot.get_current().delete_messages(
            chat_id=chat_id,
            message_ids=message_ids
        )
    except Exception as e:
        LOGGER.error(f"Error deleting messages: {e}")
