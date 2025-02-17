# -*- coding: utf-8 -*-

import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, checking_message
import os
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

log_handler = RotatingFileHandler(
    'bot.log',
    maxBytes=5 * 1024 * 1024,  # Ограничение размера файла логов до 5MB
    backupCount=5  # Количество резервных файлов
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[log_handler, console_handler]
)


async def main():
    logging.info("Запуск бота")

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=os.getenv('TOKEN'))
    dp["bot"] = bot
    dp.include_router(common.router)
    dp.include_router(checking_message.router)


    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")