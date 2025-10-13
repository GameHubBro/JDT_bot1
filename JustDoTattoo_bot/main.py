import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, calc_tattoo, gallery, studios, articles

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Открыть главное меню"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)

async def main():
    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(calc_tattoo.router)
    dp.include_router(gallery.router)
    dp.include_router(studios.router)
    dp.include_router(articles.router)

    await set_bot_commands(bot)

    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        await storage.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
