from aiogram import types
import texts.text_panel 
import inline.default_panel
from config import ADMIN

async def admin_handlers(bloom):
    @bloom.message_handler(content_types='text')
    async def text(message: types.Message):
        if message.text == 'Пользователь 🤵':
            user = message.chat.id
            await message.answer(text=texts.text_panel.message_default, reply_markup=inline.default_panel.main)

        if message.text == 'Админ 👨‍💻':
            if message.from_user.id == ADMIN:
                await bloom.bot.send_message(ADMIN, text='Вы администратор!')  # Отправка администратору
            else:
                await bloom.bot.send_message(message.chat.id, text='Вы не администратор!')  # Отправка пользователю


    admin_handlers(bloom)
