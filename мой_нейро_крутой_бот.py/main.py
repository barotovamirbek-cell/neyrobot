import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.messages import router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем обработчики яиц
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вырублен пон да")

