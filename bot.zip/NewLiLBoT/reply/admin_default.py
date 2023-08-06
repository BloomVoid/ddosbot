from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


choice_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin = KeyboardButton(text='Админ 👨‍💻')
user = KeyboardButton(text='Пользователь 🤵')
choice_panel.row(user,admin)