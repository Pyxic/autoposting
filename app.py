# bot = Bot(token=TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)
import asyncio
import time

from aiogram import executor
from tortoise import Tortoise
import aioschedule as schedule

from loader import dp
from settings import db_url
from utils import set_default_commands
import handlers


async def scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['models']},
    )
    await Tortoise.generate_schemas()
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
