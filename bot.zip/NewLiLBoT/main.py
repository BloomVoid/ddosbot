import asyncio
from concurrent.futures.thread import _shutdown
from flask import Flask
import lib.bucket
from config import TOKEN
from handler.procces_start import start_handlers
from admin.handler_default import admin_handlers
from DDosAttack.ddos_handler import ddos_attack
import sqlite3
from aiogram import types

knoo = lib.bucket.Bot(token=TOKEN)
shoot = lib.bucket.MemoryStorage()
bloom = lib.bucket.Dispatcher(knoo, storage=shoot) 



@bloom.message_handler(commands=['active'])
async def cmd_active(message: types.Message):
    try:
        database = sqlite3.connect("Bloom.sqlite")
        cursor = database.cursor()

        cursor.execute("SELECT id FROM users WHERE started = 1")
        user_ids = cursor.fetchall()

        if user_ids:
            message_text = "Привет! Это напоминание для всех участников, кто уже начал использовать бота:\n"
            for user_id in user_ids:
                message_text += f" - [id{user_id[0]}](tg://user?id={user_id[0]})\n"
            
            await bloom.bot.send_message(chat_id=message.chat.id, text=message_text, parse_mode="Markdown")
        else:
            await bloom.bot.send_message(chat_id=message.chat.id, text="Нет активных пользователей.")
    except Exception as e:
        await bloom.bot.send_message(chat_id=message.chat.id, text="Произошла ошибка при выполнении команды.")
    finally:
        cursor.close()
        database.close()


lib.bucket.logging.basicConfig(level=lib.bucket.logging.INFO)


app = Flask(__name__)
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Web Interface</title>
    </head>
    <body>
        <h1>Control Your Bot</h1>
        <p>This is a web interface for your Telegram bot.</p>
        <background = white>
    </body>
    </html>
    '''

def run_web_app():
    app.run(host='0.0.0.0', port=8745)

async def run_bot():
    await bloom.start_polling()

async def main():
    await start_handlers(bloom)
    await admin_handlers(bloom)
    await ddos_attack(bloom)


    loop = asyncio.get_event_loop()
    web_task = loop.run_in_executor(None, run_web_app)
    bot_task = asyncio.create_task(run_bot())

    # Ожидаем завершения задач
    await asyncio.gather(web_task, bot_task)

if __name__ == '__main__':
    asyncio.run(main())
