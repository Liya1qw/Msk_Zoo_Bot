from utils import bot, dp
from aiogram import types
from questins_answers import questions, que_ans
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

change_questions = {}
change_answers = {}

class AdminChange:
    @staticmethod
    async def change_que_admin(message: types.Message, state: FSMContext):
        text = 'Введите номер вопроса, который хотите поменять'
        await message.answer(text)
        await state.set_state("awaiting_admin_new_que")
    @staticmethod
    async def change_answ_admin(message: types.Message, state: FSMContext):
        text = 'Введите номер вопроса, в котором хотите изменить ответ'
        await message.answer(text)
        await state.set_state("awaiting_admin_new_answ")


@dp.message_handler(state="awaiting_admin_new_que", content_types=['text'])
async def new_que_admin(message: types.Message, state: FSMContext):
    try:
        question_number = int(message.text)
        if question_number in questions:
            await state.update_data(question_number=question_number)
            await message.answer(f'Введите новый текст для вопроса №{question_number}:')
            await state.set_state("awaiting_admin_new_que_text")
        else:
            await message.answer('Неверный номер вопроса. Пожалуйста, введите номер от 1 до 6')
    except ValueError:
        await message.answer('Введите корректный номер вопроса')

@dp.message_handler(state="awaiting_admin_new_que_text", content_types=['text'])
async def save_new_question(message: types.Message, state: FSMContext):
    new_question = message.text
    data = await state.get_data()
    question_number = data.get('question_number')

    if question_number is not None:
        questions[question_number] = new_question
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_ques = types.InlineKeyboardButton('Изменить вопрос', callback_data='change_ques')
        btn_answ = types.InlineKeyboardButton('Изменить ответ', callback_data='change_answ')
        btn_stor = types.InlineKeyboardButton('Посмотреть отзывы', callback_data='look_stor')
        btn_exit = types.InlineKeyboardButton('Выйти из режима админа', callback_data='exit_admin')
        markup.add(btn_ques, btn_answ, btn_stor, btn_exit)

        await message.answer(f'Вопрос №{question_number + 1} изменён на:\n"{new_question}"', reply_markup=markup)
    else:
        await message.answer('Ошибка: Не удалось найти номер вопроса.')
    await state.finish()

@dp.message_handler(state="awaiting_admin_new_answ", content_types=['text'])
async def select_question_for_answer_change(message: types.Message, state: FSMContext):
    try:
        question_number = int(message.text)
        if question_number in que_ans:
            await state.update_data(question_number=question_number)
            answers_list = "\n".join([f"{idx + 1}. {answer}" for idx, answer in enumerate(que_ans[question_number])])
            await message.answer(f'Введите номер ответа в вопросе №{number_que}:')
            await state.set_state("awaiting_admin_new_answ_num")
        else:
            await message.answer('Неверный номер ответа. Пожалуйста, введите номер от 1 до 5')
    except ValueError:
        await message.answer('Введите корректный номер ответа')

@dp.message_handler(state="awaiting_admin_new_answ_num", content_types=['text'])
async def select_answer_to_change(message: types.Message, state: FSMContext):
    try:
        answer_number = int(message.text) - 1
        data = await state.get_data()
        question_number = data.get('question_number')
        if question_number is not None and 0 <= answer_number < len(que_ans[question_number]):
            await state.update_data(answer_number=answer_number)
            await message.answer(
                f'Введите новый текст для ответа №{answer_number + 1} в вопросе №{question_number + 1}:')
            await state.set_state("awaiting_admin_new_answ_text")
        else:
            await message.answer('Неверный номер ответа. Пожалуйста, введите номер от 1 до 5.')
    except ValueError:
        await message.answer('Введите корректный номер ответа.')


@dp.message_handler(state="awaiting_admin_new_answ_text", content_types=['text'])
async def save_new_answer(message: types.Message, state: FSMContext):
    new_answer = message.text

    data = await state.get_data()
    question_number = data.get('question_number')
    answer_number = data.get('answer_number')

    if question_number is not None and answer_number is not None:
        que_ans[question_number][answer_number] = new_answer
        updated_answers = "\n".join([f"{idx + 1}. {ans}" for idx, ans in enumerate(que_ans[question_number])])
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_ques = types.InlineKeyboardButton('Изменить вопрос', callback_data='change_ques')
        btn_answ = types.InlineKeyboardButton('Изменить ответ', callback_data='change_answ')
        btn_stor = types.InlineKeyboardButton('Посмотреть отзывы', callback_data='get_reviews')
        btn_exit = types.InlineKeyboardButton('Выйти из режима админа', callback_data='exit_admin')
        markup.add(btn_ques, btn_answ, btn_stor, btn_exit)
        await message.answer(f'Ответ №{answer_number + 1} изменён на:\n"{new_answer}"\n\nОбновлённый список ответов:\n{updated_answers}', reply_markup=markup)
    else:
        await message.answer('Ошибка: Не удалось найти номер вопроса или ответа.')
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
