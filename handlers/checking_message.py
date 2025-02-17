from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from logging_config import setup_logging
import os

from generate_team import TeamGenerator


logger = setup_logging()

class AddTask(StatesGroup):
    get_number_participants = State()
    get_xlsx_file = State()


router = Router()

@router.message(Command(commands=['gen']))
async def get_task(message: Message, state: FSMContext):
    try:
        await state.set_state(AddTask.get_number_participants)
        await message.answer(
            text='Введите кол-во человек в одной команде:'
        )
    except Exception as e:
        logger.error(e)
        await message.answer(
            text='Ой, простите, но у меня произошла какая-то ошибка, попробуйте еще раз. Если ситуация не изменилась, '
                 'пожалуйста напишите в поддержку, чтоб они скорее все исправили.'
        )


@router.message(AddTask.get_number_participants)
async def get_task(message: Message, state: FSMContext):
    try:
        int(message.text)
        await state.update_data(quantity=message.text)

        await message.answer(
            text='Отлично! Теперь отправьте файл со списком участников в формате xlsx'
        )
        await state.set_state(AddTask.get_xlsx_file)
    except Exception as e:
        if 'invalid literal for int() with base 10:' in str(e):
            await message.answer(
                text='Отправьте число участников. ЧИСЛО!!! НЕ символ, НЕ знак, а ЧИСЛО.'
            )
        else:
            logger.error(e)
            await message.answer(
                text='Ой, простите, но у меня произошла какая-то ошибка, попробуйте еще раз. Если ситуация не изменилась, '
                     'пожалуйста напишите в поддержку, чтоб они скорее все исправили.'
            )

@router.message(AddTask.get_xlsx_file)
async def get_task(message: Message, state: FSMContext):
    try:
        bot = message.bot
        document = message.document
        if not document.file_name.endswith(('.xlsx', '.xls')):
            await message.reply("Пожалуйста, отправьте файл в формате Excel (.xlsx или .xls).")
            return

        data = await state.get_data()
        file_path = os.path.join('uploaded_files', document.file_name)
        file_info = await bot.get_file(document.file_id)
        await bot.download(file_info, file_path)

        await message.reply("Файл получен! Генерирую команды...")
        teamGen = TeamGenerator()
        result_file = teamGen.generate_team(file_path, int(data['quantity']))

        await message.answer_document(document=FSInputFile(result_file), caption="Вот таблица с командами! 🎉")
        await state.clear()
    except Exception as e:
        logger.error(e)
        await message.answer(
            text='Ой, простите, но у меня произошла какая-то ошибка, попробуйте еще раз. Если ситуация не изменилась, '
                 'пожалуйста напишите в поддержку, чтоб они скорее все исправили.'
        )