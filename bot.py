import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен вашего бота
TOKEN = "9194928064:AAF_gHnRxhFqf53fh5BFM_dcQLoIUpBYWnE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Информация по вашим адресам
INFO_1 = (
    "📍 **Адрес:** ул. Мира, 7, Синельниково\n"
    "⚡ **Группа:** 1.1 (YASNO)\n"
    "🔗 **Проверить график:** [Сайт YASNO Днепр](https://yasno.com.ua/rough-outages)"
)

INFO_2 = (
    "📍 **Адрес:** ул. Чехова, 4, Синельниково\n"
    "⚡ **Группа:** 5.2 (Укрзализныця)\n"
    "🔗 **Официальный график УЗ:** [Ссылка на график УЗ](https://www.uz.gov.ua/about/activity/electropostachannia/electro_consumers/temporary_shutdown/grafikiobmezhen/622248/)"
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Мира, 7 (Гр. 1.1)", callback_data="addr_1")
    builder.button(text="🏠 Чехова, 4 (Гр. 5.2)", callback_data="addr_2")
    builder.button(text="⚡ Показать оба графика", callback_data="addr_all")
    builder.adjust(1)

    await message.answer(
        "Привет! Я ваш бот для мониторинга отключений света в Синельниково.\n"
        "Выберите интересующий вас адрес с помощью кнопок ниже или введите /status:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    text = f"📊 **Актуальные данные по вашим объектам:**\n\n{INFO_1}\n\n-------------------\n\n{INFO_2}"
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "addr_1":
        await callback.message.answer(INFO_1, parse_mode="Markdown", disable_web_page_preview=True)
    elif callback.data == "addr_2":
        await callback.message.answer(INFO_2, parse_mode="Markdown", disable_web_page_preview=True)
    elif callback.data == "addr_all":
        await callback.message.answer(f"{INFO_1}\n\n-------------------\n\n

