from utils import dp
from aiogram import types
import random
from collections import Counter
from questins_answers import photo, questions, que_ans, question_ans1, question_ans2, question_ans3, question_ans4, question_ans5, question_ans6
from photo_answer import PhotoAnswer
from zoo_bot.admin_change import change_questions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

user_answers = {}

class Quiz:
    @staticmethod
    async def start_quiz(message: types.Message, state: FSMContext):
        await state.update_data(current_question=0)  # Начинаем с первого вопроса
        await QuizStart.show_question(message, 0)

class QuizStart:
    @staticmethod
    async def get_question(index: int):
        if index in change_questions:
            return change_questions[index]
        return questions[index]
    @staticmethod
    async def show_question(message: types.Message, question_index: int):
        ques = await QuizStart.get_question(question_index)
        markup = types.InlineKeyboardMarkup()

        for idx in range(5):
            answer = f'{que_ans.get(question_index, [])[idx]}'
            markup.add(types.InlineKeyboardButton(answer, callback_data=f'qw{question_index}_ans{idx + 1}'))
        markup.add(types.InlineKeyboardButton('Закончить викторину', callback_data='finish'))

        photo_name = photo.get(question_index, 'default')
        photo_p = f'photo/manul_{photo_name}.jpg'

        with open(photo_p, 'rb') as file:
            await message.answer_photo(file, ques, reply_markup=markup)
    # @staticmethod
    # async def question_one(message: types.Message):
    #     for i in range(len(questions)):
    #         ques = get_question(i)
    #         answers = get_answers(i)
    #
    #         markup = types.InlineKeyboardMarkup(row_width=1)
    #         ans1 = types.InlineKeyboardButton(answers[0], callback_data=f'qw{i + 1}_ans1')
    #         ans2 = types.InlineKeyboardButton(answers[1], callback_data=f'qw{i + 1}_ans2')
    #         ans3 = types.InlineKeyboardButton(answers[2], callback_data=f'qw{i + 1}_ans3')
    #         ans4 = types.InlineKeyboardButton(answers[3], callback_data=f'qw{i + 1}_ans4')
    #         ans5 = types.InlineKeyboardButton(answers[4], callback_data=f'qw{i + 1}_ans5')
    #         btn_end = types.InlineKeyboardButton('Закончить викторину', callback_data='finish')
    #         markup.add(ans1, ans2, ans3, ans4, ans5, btn_end)
    #         with open('photo/manul_agr.jpg', 'rb') as file:
    #             await message.answer_photo(file, ques, reply_markup=markup)

    # @staticmethod
    # async def question_two(message: types.Message):
    #
    #     ques = '2/6\n\nДавай лучше поговорим о твоих положительных чертах характера?'
    #     markup = types.InlineKeyboardMarkup(row_width=1)
    #     ans1 = types.InlineKeyboardButton('Я очень дружелюбный', callback_data='qw2_ans1')
    #     ans2 = types.InlineKeyboardButton('Активность - это я', callback_data='qw2_ans2')
    #     ans3 = types.InlineKeyboardButton('Спокойный как удав', callback_data='qw2_ans3')
    #     ans4 = types.InlineKeyboardButton('Легко обучаюсь новому', callback_data='qw2_ans4')
    #     ans5 = types.InlineKeyboardButton('Я просто красивый', callback_data='qw2_ans5')
    #     btn_end = types.InlineKeyboardButton('Закончить викторину', callback_data='finish')
    #     markup.add(ans1, ans2, ans3, ans4, ans5, btn_end)
    #     with open('photo/manul_smile.jpg', 'rb') as file:
    #         await message.answer_photo(file, ques, reply_markup=markup)
    #
    # @staticmethod
    # async def question_tree(message: types.Message):
    #
    #     ques = '3/6\n\nЧто тебя больше привлекает в еде?'
    #     markup = types.InlineKeyboardMarkup(row_width=1)
    #     ans1 = types.InlineKeyboardButton('Мясо, давай мясо!', callback_data='qw3_ans1')
    #     ans2 = types.InlineKeyboardButton('Рыба и морепродукты', callback_data='qw3_ans2')
    #     ans3 = types.InlineKeyboardButton('Я люблю салатики, орешки', callback_data='qw3_ans3')
    #     ans4 = types.InlineKeyboardButton('Обожаю фрукты!  Готов их есть 24/7', callback_data='qw3_ans4')
    #     ans5 = types.InlineKeyboardButton('Неприхотливый в еде', callback_data='qw3_ans5')
    #     btn_end = types.InlineKeyboardButton('Закончить викторину', callback_data='finish')
    #     markup.add(ans1, ans2, ans3, ans4, ans5, btn_end)
    #     with open('photo/manul_ask.jpg', 'rb') as file:
    #         await message.answer_photo(file, ques, reply_markup=markup)
    #
    # @staticmethod
    # async def question_four(message: types.Message):
    #
    #     ques = '4/6\n\nКуда бы ты съездил?'
    #     markup = types.InlineKeyboardMarkup(row_width=1)
    #     ans1 = types.InlineKeyboardButton('Я бы поехал в лес с палаткой', callback_data='qw4_ans1')
    #     ans2 = types.InlineKeyboardButton('В сафари. Никогда там не был', callback_data='qw4_ans2')
    #     ans3 = types.InlineKeyboardButton('Хочу плавать в океане и пить джус', callback_data='qw4_ans3')
    #     ans4 = types.InlineKeyboardButton('Устроил бы поход в горы!', callback_data='qw4_ans4')
    #     ans5 = types.InlineKeyboardButton('Джунгли, амазонка, опастность', callback_data='qw4_ans5')
    #     ans6 = types.InlineKeyboardButton('Куда-нибудь в пустыню', callback_data='qw4_ans6')
    #     btn_end = types.InlineKeyboardButton('Закончить викторину', callback_data='finish')
    #     markup.add(ans1, ans2, ans3, ans4, ans5, ans6, btn_end)
    #     with open('photo/manul_kaif.jpg', 'rb') as file:
    #         await message.answer_photo(file, ques, reply_markup=markup)
    #
    # @staticmethod
    # async def question_five(message: types.Message):
    #
    #     ques = '5/6\n\nПредставим, что сейчас уже утро, на часах 8:00. Что ты делаешь?'
    #     markup = types.InlineKeyboardMarkup(row_width=1)
    #     ans1 = types.InlineKeyboardButton('Уже утро? Ложусь спать.', callback_data='qw5_ans1')
    #     ans2 = types.InlineKeyboardButton('Зря проснулся, можно еще поспать', callback_data='qw5_ans2')
    #     ans3 = types.InlineKeyboardButton('Иду на работу', callback_data='qw5_ans3')
    #     ans4 = types.InlineKeyboardButton('Проспал! Пулей на работу', callback_data='qw5_ans4')
    #     btn_end = types.InlineKeyboardButton('Закончить викторину', callback_data='finish')
    #     markup.add(ans1, ans2, ans3, ans4, btn_end)
    #     with open('photo/manul_nedoumenie.jpg', 'rb') as file:
    #         await message.answer_photo(file, ques, reply_markup=markup)
    #
    # @staticmethod
    # async def question_six(message: types.Message):
    #
    #     ques = '6/6\n\nЧто для тебя дом?'
    #     markup = types.InlineKeyboardMarkup(row_width=1)
    #     ans1 = types.InlineKeyboardButton('Это место моей силы', callback_data='qw6_ans1')
    #     ans2 = types.InlineKeyboardButton('Это место, чтобы поспать и поесть', callback_data='qw6_ans2')
    #     ans3 = types.InlineKeyboardButton('Место, где много ценных вещей', callback_data='qw6_ans3')
    #     ans4 = types.InlineKeyboardButton('Место, где я отдыхаю от всех и вся', callback_data='qw6_ans4')
    #     btn_end = types.InlineKeyboardButton('Закончить викторину', callback_data='finish')
    #     markup.add(ans1, ans2, ans3, ans4, btn_end)
    #     with open('photo/manul_cute.jpg', 'rb') as file:
    #         await message.answer_photo(file, ques, reply_markup=markup)
    @staticmethod
    async def res_quiz(message: types.Message, state: FSMContext):
        user_data = await state.get_data()
        answers = user_data.get('answers', [])

        if not answers:
            await message.answer("No answers found.")
            return

        answers = [tuple(answer) if isinstance(answer, list) else answer for answer in answers]
        animal_count = Counter(answers)

        if not animal_count:
            await message.answer("No valid answers found.")
            return

        most_common_animal = animal_count.most_common(1)[0][0]
        chosen_animal = random.choice(most_common_animal)
        print('Юзер прошел викторину')
        await PhotoAnswer.photo_res(message, chosen_animal)


    @staticmethod
    async def store_answer(user_id, answer, state: FSMContext):
        user_data = await state.get_data()
        answers = user_data.get('answers', [])
        answers.append(answer)
        await state.update_data(answers=answers)

class QuizState(StatesGroup):
    current_question = State()

@dp.callback_query_handler(lambda call: call.data.startswith('qw'))
async def callback_qw(call: types.CallbackQuery, state: FSMContext):
    question_index, answer_index = map(int, call.data[2:].split('_ans'))

    question_ans = globals().get(f'question_ans{question_index+1}')
    if question_ans :
        answer = question_ans[answer_index]
        await QuizStart.store_answer(call.from_user.id, answer, state)

    next_question_index = question_index + 1
    await state.update_data(current_question=next_question_index)

    if next_question_index < len(questions):
        await QuizStart.show_question(call.message, next_question_index)
    else:
        await QuizStart.res_quiz(call.message, state)
# @dp.callback_query_handler(lambda call: call.data.startswith('qw1_'))
# async def callback_qw1(call: types.CallbackQuery):
#     answer_index = int(call.data.split('_ans')[1])
#
#     if answer_index in question_ans1:
#         answer.extend(question_ans1[answer_index])
#
#     await QuizStart.question_two(call.message)
#
# @dp.callback_query_handler(lambda call: call.data.startswith('qw2_'))
# async def callback_qw2(call: types.CallbackQuery):
#     answer_index = int(call.data.split('_ans')[1])
#
#     if answer_index in question_ans2:
#         answer.extend(question_ans2[answer_index])
#
#     await QuizStart.question_tree(call.message)
#
# @dp.callback_query_handler(lambda call: call.data.startswith('qw3_'))
# async def callback_qw3(call: types.CallbackQuery):
#     answer_index = int(call.data.split('_ans')[1])
#
#     if answer_index in question_ans3:
#         answer.extend(question_ans3[answer_index])
#
#     await QuizStart.question_four(call.message)
#
# @dp.callback_query_handler(lambda call: call.data.startswith('qw4_'))
# async def callback_qw4(call: types.CallbackQuery):
#     answer_index = int(call.data.split('_ans')[1])
#
#     if answer_index in question_ans4:
#         answer.extend(question_ans4[answer_index])
#
#     await QuizStart.question_five(call.message)
#
# @dp.callback_query_handler(lambda call: call.data.startswith('qw5_'))
# async def callback_qw5(call: types.CallbackQuery):
#     answer_index = int(call.data.split('_ans')[1])
#
#     if answer_index in question_ans5:
#         answer.extend(question_ans5[answer_index])
#
#     await QuizStart.question_six(call.message)
#
# @dp.callback_query_handler(lambda call: call.data.startswith('qw6_'))
# async def callback_qw6(call: types.CallbackQuery):
#     answer_index = int(call.data.split('_ans')[1])

    # if answer_index in question_ans6:
    #     answer.extend(question_ans6[answer_index])
    #
    # await QuizStart.res_quiz(call.message)
@dp.callback_query_handler(lambda call: call.data == 'finish')
async def finish_quiz(call: types.CallbackQuery):
    print('Кнопка "Закончить викторину" нажата')
    text = ('Хорошо, давай закончим викторину ☹️\n'
            'Может быть ты хотел узнать что то еще?')
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_contact = types.InlineKeyboardButton('Контакты для связи', callback_data='contacts')
    btn_help = types.InlineKeyboardButton('Помощь', callback_data='help')
    btn_back = types.InlineKeyboardButton('Назад в начало', callback_data='start')
    markup.add(btn_contact, btn_help, btn_back)
    await call.message.answer(text, reply_markup=markup)
# @dp.callback_query_handler(lambda call: call.data == 'continue')
# async def continue_quiz(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     question_number = data.get('question_number')
#
#     # await state.get_state(QuizState.current_question)
#     # await state.update_data(question_number=question_number)
#
#     if question_number == 1:
#         await QuizStart.question_one(call.message, state)
#     elif question_number == 2:
#         await QuizStart.question_two(call.message, state)
#     elif question_number == 3:
#         await QuizStart.question_tree(call.message, state)
#     elif question_number == 4:
#         await QuizStart.question_four(call.message, state)
#     elif question_number == 5:
#         await QuizStart.question_five(call.message, state)
#     elif question_number == 6:
#         await QuizStart.question_six(call.message, state)