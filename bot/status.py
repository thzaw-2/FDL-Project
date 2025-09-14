import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from bot import dp
from bot.helpers.utils import new_task
from bot.helpers.botutils import send_message
from bot.helpers.commands import BotCommands
from config import ADMINS

router = Router()

@dp.message(Command(commands=["status"], prefix=BotCommands))
@new_task
async def status_command(message: Message):
    if message.from_user.id not in ADMINS:
        await send_message(
            chat_id=message.chat.id,
            text="You do not have permission to use this command.",
            parse_mode=ParseMode.HTML
        )
        return

    args = message.text.split()
    if len(args) == 2 and args[1].lower() in ["on", "off"]:
        new_status = args[1].lower()
        os.environ['BOT_STATUS'] = new_status
        await send_message(
            chat_id=message.chat.id,
            text=f"<b>Bot status has been set to: {new_status.upper()}</b>",
            parse_mode=ParseMode.HTML
        )
        return
    
    current_status = os.environ.get("BOT_STATUS", "on").lower()
    await send_message(
        chat_id=message.chat.id,
        text=f"<b>Current bot status: {current_status.upper()}</b>\n\nUse /status on or /status off to change.",
        parse_mode=ParseMode.HTML
    )
