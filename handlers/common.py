from aiogram.filters import Command

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove


from logging_config import setup_logging

logger = setup_logging()

router = Router()

@router.message(Command(commands='start'))
async def start(message: Message):
    try:
        await message.answer(
            text='Привет. Я бот для распределения людей на команды.\n'
                 'Вызови команду /gen, для того, чтоб начать.'
        )
    except Exception as e:
        logger.exception(e)
        await message.answer(
            text='Ой, простите, но у меня произошла какая-то ошибка, попробуйте еще раз. Если ситуация не изменилась, '
                 'пожалуйста напишите в поддержку, чтоб они скорее все исправили.'
        )

