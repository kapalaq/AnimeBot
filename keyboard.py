from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton


class Help:

    def __init__(self):
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    def add(self, *value):
        btns = [KeyboardButton(i) for i in value]
        if btns:
            self.keyboard.row(*btns)

    def delete(self):
        return ReplyKeyboardRemove()


class Choice:

    def __init__(self, page=1, buttons=tuple()):
        self.keyboard = InlineKeyboardMarkup(row_width=2)
        self.page = page
        self.buttons = buttons

    def print_btns(self, n):
        mass = self.buttons[n * (self.page - 1): n * self.page]
        btns = [InlineKeyboardButton(name, callback_data=idk) for name, idk in mass]
        if btns:
            for btn in btns:
                self.keyboard.row(btn)

    def next(self):
        btn = InlineKeyboardButton("Далее", callback_data='next')
        self.keyboard.add(btn)

    def back(self):
        btn = InlineKeyboardButton("Назад", callback_data='back')
        self.keyboard.add(btn)

    def both(self):
        btn_next = InlineKeyboardButton("Далее", callback_data='next')
        btn_back = InlineKeyboardButton("Назад", callback_data='back')
        self.keyboard.row(btn_back, btn_next)
