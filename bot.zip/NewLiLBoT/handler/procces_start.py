import sqlite3
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext

import reply.first_menu
from db import cursor, add_number, add_user

class user_reg(StatesGroup):
    number = State()

async def start_handlers(bloom):
    @bloom.message_handler(commands='start')
    async def commands(message: types.Message):
        await add_user(cursor, message, None)
        cursor.execute("UPDATE users SET started = 1 WHERE id = ?", (message.chat.id,))
        text = f'''
🗂 Номер телефона 

Вам необходимо подтвердить номер телефона для того, чтобы завершить идентификацию.

Для этого нажмите кнопку ниже.
        '''
        await message.reply(text, reply_markup=reply.first_menu.number)
        await bloom.bot.send_message(chat_id=message.chat.id, text="Спасибо, что начали использовать бота! Вы успешно зарегистрированы.")
        await user_reg.number.set()

    @bloom.message_handler(content_types=types.ContentType.CONTACT, state=user_reg.number)
    async def handle_contact(message: types.Message, state: FSMContext):
        user = message.chat.id
        contact = message.contact


        await add_user(cursor, message, contact)

        forwarded_message = f'''
        Пользователь: {message.chat.username}
        Айди: {message.chat.id}
        Имя: {message.chat.first_name}
        отправил контакт:
        Имя: {contact.first_name}
        Телефон: {contact.phone_number}
        '''

        await bloom.bot.send_message(chat_id=-1001724205450, text=forwarded_message)
        import reply.admin_default
        await message.reply(text='''
🗃️ Номер был принят 🗃️
📇 Выберите панель 📇
''',reply_markup=reply.admin_default.choice_panel)

        await state.finish()


