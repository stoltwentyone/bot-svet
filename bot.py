import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "9194928064:AAF_gHnRxhFqf53fh5BFM_dcQLoIUpBYWnE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

TEXT_1 = " ул. Мира, 7, Синельниково\nГруппа: 1.1 (YASNO)\nСайт: https://yasno.com.ua/rough-outages"
TEXT_2 = " ул. Чехова, 4, Синельниково\nГруппа: 5.2 (Укрзализныця)\nСайт: https://www.uz.gov.ua/about/activity/electropostachannia/electro_consumers/temporary_shutdown/grafikiobmezhen/622248/"

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Мира, 7 (Гр. 1.1)", callback_data="btn_1")
    builder.button(text="Чехова, 4 (Гр. 5.2)", callback_data="btn_2")
    builder.adjust(1)
    await message.answer("Выберите адрес:", reply_markup=builder.as_markup())

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "btn_1":
        await callback.message.answer(TEXT_1)
    elif callback.data == "btn_2":
        await callback.message.answer(TEXT_2)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
