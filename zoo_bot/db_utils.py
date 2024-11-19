import aiosqlite
from utils import bot, dp
from aiogram import types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

DB_PATH = 'reviews.sql'

async def create_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            review_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        await db.commit()
        print("Таблица создана.")

async def add_review(user_id, username, review_text):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('INSERT INTO reviews (user_id, username, review_text) VALUES (?, ?, ?)', (user_id, username, review_text))
            await db.commit()
    except Exception as e:
        print(f"Ошибка при добавлении отзыва: {e}")

async def get_reviews():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('SELECT user_id, review_text, timestamp FROM reviews')
        reviews = await cursor.fetchall()
    return reviews


async def save_review(message: types.Message, state: FSMContext):
    review_text = message.text.strip()
    if not review_text:
        await message.answer("Пожалуйста, напишите текст отзыва.")
        return

    user_id = message.from_user.id
    username = message.from_user.username or "Аноним"

    # Сохраняем отзыв
    await add_review(user_id, username, review_text)

    # Отправляем благодарность
    await message.answer(f"Спасибо за ваш отзыв, {message.from_user.first_name}!")
    await state.finish()