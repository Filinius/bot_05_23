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
#    sex = State()
    exercise = State()
    exercise_result = State()


async def on_startup(_):
    try:
        await db.create_table_user()
        logging.info("Подключение к БД выполнено успешно")
    except Exception as e:
        logging.exception(e)


async def start_handler(message: types.Message):
    # db.add_id_user_full_name(message.from_user.id, message.from_user.full_name)
    db.add_user(message.from_user.id, message.from_user.full_name)
    name = message.from_user.full_name
    await message.answer(f"Привет {name}! Я помогу тебе узнать на баллов "
                         f"выполнено упражнение.\nНажми /calc, чтобы начать.")


# async def auth_sex(message: types.Message):
#     buttons = [
#         types.InlineKeyboardButton(text="Муж.", callback_data="sex_m"),
#         types.InlineKeyboardButton(text="Жен.", callback_data="sex_w")
#     ]
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*buttons)
#
#     await message.answer(f"Выберите пол:", reply_markup=keyboard)
#     await AuthStates.sex.set()


#async def auth_sex_callback(callback_query: types.CallbackQuery, state: FSMContext):
    # sex_dict = {
    #     "m": "муж",
    #     "w": "жен"
    # }
    # sex = sex_dict[callback_query.data[4:]]
    # await state.update_data(sex=sex)
    # await bot.answer_callback_query(callback_query.id)
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


async def auth_exercise_callback(callback_query: types.CallbackQuery, state: FSMContext):
    exercise_dict = {
        "run_100": "бег на 100 м",
        "pull_up": "подтягивание на перекладине",
        "marsh_for_5": "марш-бросок на 5 км"
    }
    exercise = exercise_dict[callback_query.data[9:]]
    await state.update_data(exercise=exercise)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите результат выполения упражнения {exercise}")
    await AuthStates.exercise_result.set()


async def auth_exercise_result(message: types.Message, state: FSMContext):
    exercise_result = float(message.text.strip())
    await state.update_data(exercise_result=exercise_result)
    data = await state.get_data()
#    sex = data['sex']
    exercise = data['exercise']
#    exercise_result = data['exercise_result']
    user_id = message.from_user.id
    db.add_exercise_exercise_result(exercise, exercise_result, user_id)
    point = db.calc_result()[0]
    print(point) # для отладки
    print(type(exercise_result)) # для отладки
    await message.answer(
        f"Название упражнения: {exercise}\nРезультат выполнения упражнения: {exercise_result}\nКоличество баллов: {point}")
    await state.finish()
    # await state.reset_state(with_data=True)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(auth_exercise, commands="calc")
#    dp.register_callback_query_handler(auth_sex_callback, lambda c: c.data and c.data.startswith('sex_'),
#                                       state=AuthStates.sex)
    dp.register_callback_query_handler(auth_exercise_callback, lambda c: c.data and c.data.startswith('exercise_'),
                                       state=AuthStates.exercise)
    dp.register_message_handler(auth_exercise_result, state=AuthStates.exercise_result)


if __name__ == '__main__':
    register_handlers(dp=dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

