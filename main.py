import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
from pandas_processing import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class AuthStates(StatesGroup):

    exercise = State()
    exercise_result = State()


async def on_startup(_):
    pass
    # try:
    #     await db.create_table_user()
    #     logging.info("Подключение к БД выполнено успешно")
    # except Exception as e:
    #     logging.exception(e)


async def start_handler(message: types.Message):
    name = message.from_user.full_name
    await message.answer(f"Привет {name}! Я помогу тебе узнать на баллов "
                         f"выполнено упражнение.\nНажми /calc, чтобы начать.")


async def auth_exercise(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Бег на 100 м", callback_data="exercise_run_100"),
        types.InlineKeyboardButton(text="Подтягивание на перекладине", callback_data="exercise_pull_up"),
        types.InlineKeyboardButton(text="Марш-бросок на 5 км", callback_data="exercise_marsh_for_5")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await message.answer(f"Выберите упражнение:", reply_markup=keyboard)

    await AuthStates.exercise.set()

exercise_dict = {
    "run_100": "бег на 100 м",
    "pull_up": "подтягивание на перекладине",
    "marsh_for_5": "марш-бросок на 5 км"
}
async def auth_exercise_callback(callback_query: types.CallbackQuery, state: FSMContext):

    exercise = callback_query.data[9:]
    exercise_d = exercise_dict[exercise]
    await state.update_data(exercise=exercise)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите результат выполения упражнения {exercise_d}")
    await AuthStates.exercise_result.set()


async def auth_exercise_result(message: types.Message, state: FSMContext):
    exercise_result = message.text.strip()
    await state.update_data(exercise_result=exercise_result)
    data = await state.get_data()
    exercise = data['exercise']
    exercise_d = exercise_dict[exercise]
    print(exercise)

    #user_id = message.from_user.id

    #db.add_exercise_exercise_result(exercise, exercise_result, user_id)

    print(exercise_result)
    #point = db.calc_result(exercise)[0]





    print(type(exercise_result)) # для отладки
    await message.answer(
        f"Название упражнения: {exercise_d}\nРезультат выполнения упражнения: {exercise_result}\nКоличество баллов: ")
    await state.finish()
    # await state.reset_state(with_data=True)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(auth_exercise, commands="calc")
    dp.register_callback_query_handler(auth_exercise_callback, lambda c: c.data and c.data.startswith('exercise_'),
                                       state=AuthStates.exercise)
    dp.register_message_handler(auth_exercise_result, state=AuthStates.exercise_result)


if __name__ == '__main__':
    register_handlers(dp=dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

