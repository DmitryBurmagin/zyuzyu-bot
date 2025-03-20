from aiogram import types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Загрузить файл", callback_data="upload_file")]
        ]
    )
    await message.answer("Привет, жми кнопку и загружай файл!", reply_markup=keyboard)


async def process_upload(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Отправьте файл формата Excel.")


def register_handlers(dp):
    dp.message.register(cmd_start, Command("start"))
    dp.callback_query.register(process_upload, lambda c: c.data == 'upload_file')
