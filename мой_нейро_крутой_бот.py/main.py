import os
import subprocess
import sys
import logging

# --- ПРИНУДИТЕЛЬНАЯ УСТАНОВКА ---
def install_libs():
    libs = ["aiogram==3.17.0", "groq==0.15.0"]
    for lib in libs:
        try:
            # Проверка наличия
            if "groq" in lib: __import__("groq")
            if "aiogram" in lib: __import__("aiogram")
        except ImportError:
            logging.info(f"Установка {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

logging.basicConfig(level=logging.INFO)
install_libs()

# --- ОСНОВНОЙ КОД ---
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.messages import router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот проснулся!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
