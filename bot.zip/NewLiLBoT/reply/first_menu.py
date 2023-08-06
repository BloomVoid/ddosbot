from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


number = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Подтвердить ✅',request_contact=True)
number.add(button)