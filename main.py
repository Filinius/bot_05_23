import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
from pandas_processing import PandasCalc

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
df = PandasCalc('Data/102.xlsx')


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
    await message.answer(f"Привет {name}!\nОнлайн калькулятор\n "
                         f"По физической подготовке\n"
                         f"НФП-2013\n"
                         f"Нажми /calc, чтобы начать.")


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


    timess = ['run_100', 'marsh_for_5']

    if exercise == 'pull_up':
        try:
            exercise_result = int(message.text.strip())
            exercise_points = df.calc_result_reps(exercise, exercise_result)
        except ValueError:
            await message.answer(f"Введено некорректное значение!\n"
                                 f"Введите количество повторений упражнения {exercise_d.upper()}."
                                 f"\n<u>Например: 15</u>", parse_mode=types.ParseMode.HTML)
            return

    elif exercise in timess:
        try:
            exercise_result = float(exercise_result.strip().replace(",", ".").replace(":", "."))
            exercise_points = df.calc_result_time(exercise, exercise_result)
        except ValueError:
            await message.answer(f"Введено некорректное значение!\n"
                                 f"Введите результат выполнения упражнения {exercise_d.upper()} в виде числа."
                                 f"\n<u>Например: 12.25</u>", parse_mode=types.ParseMode.HTML)
            return

    print(exercise_result)
    # point = db.calc_result(exercise)[0]

    print(type(exercise_result))  # для отладки
    await message.answer(
        f"Упражнение:\n{exercise_d.upper()}\n"
        f"Результат: {exercise_result}\n"
        f"Количество баллов: {exercise_points}")
    await state.finish()
    # await state.reset_state(with_data=True)

async def random_text(message:types.Message):
    name = message.from_user.full_name
    await message.answer(f"👋Привет {name}!\nОнлайн калькулятор\n"
                         f"По физической подготовке\n"
                         f"НФП-2013\n"
                         f"Нажми /calc, чтобы начать.")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(auth_exercise, commands="calc")
    dp.register_callback_query_handler(auth_exercise_callback, lambda c: c.data and c.data.startswith('exercise_'),
                                       state=AuthStates.exercise)
    dp.register_message_handler(auth_exercise_result, state=AuthStates.exercise_result)
    dp.register_message_handler(random_text)


if __name__ == '__main__':
    register_handlers(dp=dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
