from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class AuthStates(StatesGroup):
    name = State()
    exercise = State()
    exercise_result = State()


async def start_handler(message: types.Message):
    await message.answer("Привет! Я помогу тебе авторизоваться. Нажми /auth, чтобы начать")


async def auth_start(message: types.Message):
    await message.answer("Введите свое имя")
    await AuthStates.name.set()


async def auth_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f"Привет {name}!\nВведи название упражнения")
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
    name = data['name']
    exercise = data['exercise']
    exercise_result = data['exercise_result']

    # await message.answer(f"{data['name']}. Название упражнения: {data['exercise']}\nРезультат выполнения
    # упражнения: {data['exercise_result']}")
    await message.answer(f"{name}. Название упражнения: {exercise}\nРезультат выполнения упражнения: {exercise_result}")
    await state.finish()
    # await state.reset_state(with_data=True)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(auth_start, commands="auth")
    dp.register_message_handler(auth_name, state=AuthStates.name)
    dp.register_message_handler(auth_exercise, state=AuthStates.exercise)
    dp.register_message_handler(auth_exercise_result, state=AuthStates.exercise_result)


if __name__ == '__main__':
    register_handlers(dp=dp)
    executor.start_polling(dp,
                           skip_updates=True)  # skip_updates=True пропустить все обновления, которые бот пропустил
    # во время отключения
'''
12121212121212
'''