import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.messages import router

# Настройка логирования для отслеживания ошибок в консоли BotHost
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)
    
    # Инициализация диспетчера
    dp = Dispatcher()
    
    # Подключаем наш роутер с логикой Groq
    dp.include_router(router)

    logging.info("Бот на Groq запущен!")
    
    # Очищаем очередь старых сообщений и запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен спатке")
    except Exception as e:
        logging.error(f"Критическая ошибка при запуске зовите майсера: {e}")

