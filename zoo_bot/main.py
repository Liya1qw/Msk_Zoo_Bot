from aiogram import executor, types
from utils import dp
from zoo_bot.quiz.quiz_bot import Quiz
from cont_zoo import ContZoo
from zoo_bot.admin.admin_zoo import Administrator
from aiogram.dispatcher import FSMContext
from zoo_bot.review.db_utils import create_table
from zoo_bot.review.review_user import ReviewUser

async def on_startup(dispatcher):
    await create_table()

async def send_welcome_message(message: types.Message, first_name: str):
    text = (f'Привет {first_name}! ☺️\n'
        'Рад тебя видеть! Меня зовут Тимоша и я живу в Московском зоопарке :)\n\n'
        'Недавно я прошел викторину "Кто твое тотемное животное?" и узнал, что мое тотемное животное - манул! 😱\n'
        'Предлагаю тебе тоже пройти такую викторину! Давай узнаем, кто твое тотемное животное?\n\n'
        'А в конце викторины я подготовил для тебя кое-что интересное 😋\n\n'
        'С любовью,\n'
        'Тимоша')
    with open('photo/manul_photo.jpg', 'rb') as file:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_quiz = types.InlineKeyboardButton('Начать викторину 😍', callback_data='quiz')
        btn_contact = types.InlineKeyboardButton('Контакты для связи', callback_data='contacts')
        btn_help = types.InlineKeyboardButton('Помощь', callback_data='help')
        markup.add(btn_quiz, btn_contact, btn_help)
        await message.answer_photo(file, text, reply_markup=markup)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    name_user = message.from_user.first_name
    await send_welcome_message(message, name_user)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await ContZoo.help_zoo(message)

@dp.message_handler(commands=['review'])
async def admin(message: types.Message, state: FSMContext):
    print("Кнопка 'Написать отзыв' нажата")
    await ReviewUser.review_user(message, state)

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message, state: FSMContext):
    await Administrator.administrator_zoo(message, state)

@dp.callback_query_handler(lambda call: call.data == 'quiz')
async def callback_quiz(call: types.CallbackQuery, state: FSMContext):
    print("Кнопка 'Начать викторину' нажата")
    await Quiz.start_quiz(call.message, state)

@dp.callback_query_handler(lambda call: call.data == 'contacts')
async def callback_contact(call: types.CallbackQuery):
    print("Кнопка 'Контакты для связи' нажата")
    await ContZoo.more_contact(call.message)

@dp.callback_query_handler(lambda call: call.data == 'help')
async def callback_help(call: types.CallbackQuery):
    print("Кнопка 'Помощь' нажата")
    await ContZoo.help_zoo(call.message)

@dp.callback_query_handler(lambda call: call.data == 'start')
async def callback_start(call: types.CallbackQuery):
    print("Кнопка 'Вернуться в начало' нажата")
    await send_welcome_message(call.message, f'{call.from_user.first_name}')

@dp.callback_query_handler(lambda call: call.data == 'review')
async def callback_review(call: types.CallbackQuery, state: FSMContext):
    print("Кнопка 'Написать отзыв' нажата")
    await ReviewUser.review_user(call.message, state=state)

@dp.errors_handler()
async def handle_errors(update, exception):
    print(f"Ошибка: {exception}")
    return True


executor.start_polling(dp, on_startup=on_startup)