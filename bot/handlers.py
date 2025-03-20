import os

import pandas as pd
from aiogram import types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from .parser import parse_website


async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Загрузить файл", callback_data="upload_file"
                )
            ]
        ]
    )
    await message.answer(
        "Привет, жми кнопку и загружай файл!", reply_markup=keyboard
    )


async def process_upload(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Отправьте файл формата Excel.")


async def handle_file(message: types.Message):
    if message.document:
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path

        download_folder = "./downloads"
        os.makedirs(download_folder, exist_ok=True)

        file_name = message.document.file_name
        file_extension = os.path.splitext(file_name)[1].lower()

        if file_extension not in [".xls", ".xlsx"]:
            await message.answer(
                "Отправьте документ в формате Exel (xls, xlsx)"
            )
            return

        destination_path = os.path.join(download_folder, file_name)

        await message.bot.download_file(
            file_path, destination=f"{destination_path}"
        )

        try:
            df = pd.read_excel(destination_path)

            print(df)

            for _, row in df.iterrows():
                url = row["url"].strip()
                xpath = row["xpath"].strip()
                result = await parse_website(url, xpath)
                print(f"Парсинг для {url}: {result}")

            await message.answer("Данные выведены в консоль. (Тестово)")

        except Exception as e:
            await message.answer(e)

        await message.answer(
            f"Файл {file_name} успешно загружен в {destination_path}."
        )
    else:
        await message.answer("Это не файл. Отправьте файл.")


async def is_upload_file(callback_query: types.CallbackQuery):
    return callback_query.data == "upload_file"


def register_handlers(dp):
    dp.message.register(cmd_start, Command("start"))
    dp.callback_query.register(process_upload, is_upload_file)
    dp.message.register(handle_file)
