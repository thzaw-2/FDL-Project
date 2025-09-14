# config.py
import os

# Get log channel ID from environment variables
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", -100))