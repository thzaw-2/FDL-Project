import logging
import os
from logging.handlers import RotatingFileHandler

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
LOGGER.addHandler(console_handler)

if not os.path.exists("logs"):
    os.makedirs("logs")
file_handler = RotatingFileHandler("logs/bot.log", maxBytes=1048576, backupCount=5)
file_handler.setFormatter(formatter)
LOGGER.addHandler(file_handler)
