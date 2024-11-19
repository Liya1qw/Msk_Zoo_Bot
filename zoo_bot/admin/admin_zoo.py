from utils import dp
from aiogram import types
from zoo_bot.admin.admin_change import AdminChange
from aiogram.dispatcher import FSMContext
from db_utils import get_reviews

class Administrator:
    @staticmethod
    async def administrator_zoo(message: types.Message, state: FSMContext):
        text = 'Введи ключ к доступу администратирования'
        await message.answer(text)
        await state.set_state("awaiting_admin_key")


@dp.message_handler(state="awaiting_admin_key", content_types=['text'])
async def key_admin(message: types.Message, state: FSMContext):
    key = '9yuhs14_oplf53w0/po1'
    if message.text.strip() == key:
        text = 'Привет! Теперь у тебя есть доступ к изменениям вопросов квиза, ответов на вопросы, а так же ты можешь посмотреть отзывы.'
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_ques = types.InlineKeyboardButton('Изменить вопрос', callback_data='change_ques')
        btn_answ = types.InlineKeyboardButton('Изменить ответ', callback_data='change_answ')
        btn_stor = types.InlineKeyboardButton('Посмотреть отзывы', callback_data='get_reviews')
        btn_exit = types.InlineKeyboardButton('Выйти из режима админа', callback_data='exit_admin')
        markup.add(btn_ques, btn_answ, btn_stor, btn_exit)
        await message.answer(text, reply_markup=markup)
        await state.set_state("admin_mode")
    else:
        await message.answer('Ошибка доступа. Неверный ключ.')
        await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'exit_admin', state="admin_mode")
async def exit_admin_mode(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    try:
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('Назад в начало', callback_data='start')
        markup.add(btn_back)
        await call.message.answer('Вы вышли из режима администратора.', reply_markup=markup)
        await state.finish()
    except KeyError:
        pass

@dp.callback_query_handler(lambda call: call.data == 'change_ques', state="admin_mode")
async def change_que(call: types.CallbackQuery, state: FSMContext):
    await AdminChange.change_que_admin(call.message, state)

@dp.callback_query_handler(lambda call: call.data == 'change_answ', state="admin_mode")
async def change_ans(call: types.CallbackQuery, state: FSMContext):
    await AdminChange.change_answ_admin(call.message, state)

@dp.callback_query_handler(lambda call: call.data == 'get_reviews', state="admin_mode")
async def show_reviews(call: types.CallbackQuery):
        reviews = await get_reviews()
        if not reviews:
            await call.message.answer("Пока нет отзывов.")
        else:
            review_texts = [
                f"👤 <b>{username}</b>\n📝 {review}\n⏰ {timestamp}"
                for username, review, timestamp in reviews
            ]
            await call.message.answer("\n\n".join(review_texts), parse_mode="HTML")
        for username, review_text, timestamp in reviews:
            print(f"👤 {username}, 📝 {review_text}, ⏰ {timestamp}")