from utils import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from db_utils import add_review, get_reviews, create_table, save_review

class ReviewUser:
    @staticmethod
    async def review_user(message: types.Message, state: FSMContext):
        if await state.get_state():
            await state.finish()  # Завершаем любое предыдущее состояние
        await message.answer("Пожалуйста, напишите ваш отзыв. По желанию, для обратной связи по вашему отзыву, можете оставить еще ваш номер телефона :)")
        await state.set_state("awaiting_review")

    @staticmethod
    async def review_user_admin(message: types.Message):
        reviews = get_reviews()

        if not reviews:
            await message.answer("Отзывы пока отсутствуют.")
        else:
            reviews_text = "\n\n".join([f"Пользователь {r[0]}:\n{r[1]}\n{r[2]}" for r in reviews])
            await message.answer(f"Отзывы:\n\n{reviews_text}")

@dp.message_handler(state="awaiting_review", content_types=types.ContentType.ANY)
async def save_review_user(message: types.Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("Пожалуйста, отправьте текстовый отзыв.")
        return
    await save_review(message, state)

@dp.errors_handler()
async def handle_errors(update, exception):
    print(f"Ошибка: {exception}")
    return True
