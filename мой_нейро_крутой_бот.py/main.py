import subprocess
import sys
import logging

# --- БЛОК АВТОУСТАНОВКИ (решает проблему от которой я в ахуе) ---
def install_dependencies():
    packages = ["aiogram", "google-generativeai"]
    for package in packages:
        try:
            if package == "google-generativeai":
                __import__("google.generativeai")
            else:
                __import__(package)
        except ImportError:
            print(f"Установка {package} через pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Запускаем установку мистер фурри 
install_dependencies()
# -------------------------------------------------------------

import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.messages import router

# Настройка логирования, чтобы видеть ошибки в консоли хостинга
logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутер с логикой ИИ
    dp.include_router(router)

    print("Бот запущен и готов к работе!")
    
    # Пропускаем накопившиеся сообщения и запускаем опрос
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот пошел спать")
    except Exception as e:
        print(f"Критический пиздец зовите майсера: {e}")
