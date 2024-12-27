from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import ApiKey
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ApiKey.apiKey
bot = Bot(token=api)

dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

inline_keyboard = InlineKeyboardMarkup()

inline_keyboard.row(InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="Calories"), InlineKeyboardButton(text="Формулы расчета", callback_data="formulas"))

calories_button = KeyboardButton(text="Расчитать")
start_button = KeyboardButton(text="/start")
info_button = KeyboardButton(text="Информация")

start_keyboard.add(start_button)
main_keyboard.row(calories_button, info_button)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dispatcher.message_handler(text="Расчитать")
async def main_menu(ms):
    await ms.answer("Выберите опцию:", reply_markup=inline_keyboard)



@dispatcher.callback_query_handler(text="Calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()
    await call.answer()

@dispatcher.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()

@dispatcher.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dispatcher.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dispatcher.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        await message.answer(
            f"Ваша норма калирий {float(data['weight']) * 10 + float(data['growth']) * 6.25 - float(data['age']) * 5 + 5}")
    except ValueError:
        await message.answer("Вы ввели не верные данные")
    finally:
        await state.finish()


@dispatcher.message_handler(commands="start")
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=main_keyboard)


@dispatcher.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.", reply_markup = start_keyboard)


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
