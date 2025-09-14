from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class SmartButtons:
    def __init__(self):
        self.buttons = []

    def button(self, text: str, url: str = None, callback_data: str = None):
        if url:
            self.buttons.append(InlineKeyboardButton(text=text, url=url))
        elif callback_data:
            self.buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))

    def build_menu(self, b_cols: int = 1):
        menu = [self.buttons[i:i + b_cols] for i in range(0, len(self.buttons), b_cols)]
        return InlineKeyboardMarkup(inline_keyboard=menu)
