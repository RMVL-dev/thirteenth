from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import ApiKey
from aiogram.dispatcher.filters.state import State, StatesGroup

api = ApiKey.apiKey
bot = Bot(token=api)

dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dispatcher.message_handler(text="Calories")
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()


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
    await message.answer(f"Ваша норма калирий {float(data['weight']) * 10 + float(data['growth']) * 6.25 - float(data['age']) * 5 + 5}")
    await state.finish()

@dispatcher.message_handler(commands="start")
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dispatcher.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
