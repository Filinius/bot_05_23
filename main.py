import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
from sqlite_bd import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database('new.db')


class AuthStates(StatesGroup):
    sex = State()
    exercise = State()
    exercise_result = State()


async def on_startup(_):
    try:
        await db.create_table_user()
        logging.info("Подключение к БД выполнено успешно")
    except Exception as e:
        logging.exception(e)


async def start_handler(message: types.Message):
    db.add_id_user_full_name(message.from_user.id, message.from_user.full_name)
    name = message.from_user.full_name
    await message.answer(f"Привет {name}! Я помогу тебе подсчитать количество набранных баллов по результатам "
                         f"выполненных упражнений.\nНажми /auth, чтобы начать.")


async def auth_start(message: types.Message):
    await message.answer("Введите свой пол.")
    await AuthStates.sex.set()


async def auth_sex(message: types.Message, state: FSMContext):
    sex = message.text
    await state.update_data(sex=sex)
    await message.answer(f"Ваш пол {sex}!\nВведи название упражнения")
    await AuthStates.exercise.set()


async def auth_exercise(message: types.Message, state: FSMContext):
    exercise = message.text
    await state.update_data(exercise=exercise)
    await message.answer(f"Введите результат выполения упражнения {exercise}")
    await AuthStates.exercise_result.set()


async def auth_exercise_result(message: types.Message, state: FSMContext):
    exercise_result = message.text
    await state.update_data(exercise_result=exercise_result)
    data = await state.get_data()
    sex = data['sex']
    exercise = data['exercise']
    exercise_result = data['exercise_result']

    await message.answer(
        f"Ваш пол {sex}.\nНазвание упражнения: {exercise}\nРезультат выполнения упражнения: {exercise_result}")
    await state.finish()
    # await state.reset_state(with_data=True)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(auth_start, commands="auth")
    dp.register_message_handler(auth_sex, state=AuthStates.sex)
    dp.register_message_handler(auth_exercise, state=AuthStates.exercise)
    dp.register_message_handler(auth_exercise_result, state=AuthStates.exercise_result)


if __name__ == '__main__':
    register_handlers(dp=dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # skip_updates=True пропустить все
    # обновления, которые бот пропустил во время отключения
