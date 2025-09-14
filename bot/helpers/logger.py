# bot/helpers/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

# Create a logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
LOGGER.addHandler(console_handler)

# Create a file handler
if not os.path.exists("logs"):
    os.makedirs("logs")
file_handler = RotatingFileHandler("logs/bot.log", maxBytes=1048576, backupCount=5)
file_handler.setFormatter(formatter)
LOGGER.addHandler(file_handler)