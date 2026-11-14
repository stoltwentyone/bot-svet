import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "9194928064:AAF_gHnRxhFqf53fh5BFM_dcQLoIUpBYWnE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

INFO_1 = (
    "📍 **ул. Мира, 7, Синельниково**\n"
    "⚡ Группа: 1.1 (YASNO)\n\n"
    "📋 **График отключений:**\n"
    "• 00:00 - 04:00 | Без света\n"
    "• 04:00 - 08:00 | С сомнением / Возможны отключения\n"
    "• 08:00 - 12:00 | Есть свет\n"
    "• 12:00 - 16:00 | Без света\n"
    "• 16:00 - 20:00 | Есть свет\n"
    "• 20:00 - 24:00 | Без света\n\n"
    "🔗 Официальный сайт YASNO: https://yasno.com.ua/rough-outages"
)

INFO_2 = (
    "📍 **ул. Чехова, 4, Синельниково**\n"
    "⚡ Группа: 5.2 (Укрзализныця)\n\n"
    "📋 **График отключений:**\n"
    "• 02:00 - 06:00 | Без света\n"
    "• 06:00 - 10:00 | Есть свет\n"
    "• 10:00 - 14:00 | Без света\n"
    "• 14:00 - 18:00 | Есть свет\n"
    "• 18:00 - 22:00 | Без света\n"
    "• 22:00 - 02:00 | Есть свет\n\n"
    "🔗 Официальный сайт Укрзализныци: https://www.uz.gov.ua/about/activity/electropostachannia/electro_consumers/temporary_shutdown/grafikiobmezhen/622248/"
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Мира, 7 (Гр. 1.1)", callback_data="btn_1")
    builder.button(text="Чехова, 4 (Гр. 5.2)", callback_data="btn_2")
    builder.adjust(1)
    await message.answer("🏠 Выберите нужный адрес, чтобы сразу увидеть график:", reply_markup=builder.as_markup())

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "btn_1":
        await callback.message.answer(INFO_1, parse_mode="Markdown")
    elif callback.data == "btn_2":
        await callback.message.answer(INFO_2, parse_mode="Markdown")
    await callback.answer()

# Веб-сервер для Render
async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")

async def main():
    # Запускаем веб-сервер и поллинг бота параллельно
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
