import os

LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", -100))

# ADMINS variable ကို တန်ဖိုးမရှိရင် list အလွတ်တစ်ခု ပြန်ပေးပါ
admins_str = os.environ.get("ADMINS", "")
ADMINS = list(map(int, admins_str.split(','))) if admins_str else []

BOT_STATUS = os.environ.get("BOT_STATUS", "on").lower()
