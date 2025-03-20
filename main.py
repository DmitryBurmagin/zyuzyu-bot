import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import register_handlers

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    raise ValueError("API_TOKEN not found in .env file")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

register_handlers(dp)


async def on_start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    from asyncio import run

    run(on_start())
