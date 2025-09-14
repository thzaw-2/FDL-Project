import os

LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", -100))
ADMINS = list(map(int, os.environ.get("ADMINS", "").split(',')))
BOT_STATUS = os.environ.get("BOT_STATUS", "on").lower()
