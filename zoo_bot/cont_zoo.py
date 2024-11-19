from utils import bot, dp
from aiogram import types

class ContZoo:
    @staticmethod
    async def more_contact(message: types.Message):
        try:
            text_other = ('Смотри что тут у нас есть 🤗\n\n'
                          'Я оставил для тебя контакты домика, где я живу. Вдруг ты захочешь спросить как у меня дела или прийти ко мне в гости :)\n\n'
                          'А еще у нас есть замечательная программа для наших друзей! Она называется "Клуб друзей". Ты можешь взять любое животное под опеку 😍\n'
                          'Тыкай скорее по кнопке "Клуб друзей", чтобы узнать больше о программе.')
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn_more_cont = types.InlineKeyboardButton('Еще контакты для связи', url='https://moscowzoo.ru/contacts')

            btn_friend = types.InlineKeyboardButton('Круг друзей 🫰🏻', url='https://moscowzoo.ru/about/guardianship')
            btn_tg = types.InlineKeyboardButton('Телеграмм-канал Московского зоопарка',
                                                url='https://t.me/Moscowzoo_official')
            btn_site = types.InlineKeyboardButton('Сайт Московского зоопарка', url='https://moscowzoo.ru/')
            btn_back = types.InlineKeyboardButton('Назад в начало', callback_data='start')
            markup.add(btn_more_cont, btn_friend, btn_tg, btn_site, btn_back)
            await message.answer(text_other, reply_markup=markup)
        except Exception as e:
            print(f"Ошибка в more_contact: {e}")
            await message.answer("Произошла ошибка при попытке показать контакты.")

    @staticmethod
    async def help_zoo(message: types.Message):
        text_help = ('Для удобства, у меня есть несколько кнопок и комманд:\n'
                     '/start - запуск бота\n'
                     '/help - помощь\n'
                     '/review - написать отзыв\n'
                     '/admin - администратор')
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_quiz = types.InlineKeyboardButton('Начать викторину 😍', callback_data='quiz')
        btn_contact = types.InlineKeyboardButton('Контакты для связи', callback_data='contacts')
        btn_help = types.InlineKeyboardButton('Помощь', callback_data='help')
        btn_back = types.InlineKeyboardButton('Назад в начало', callback_data='start')
        markup.add(btn_quiz, btn_contact, btn_help, btn_back)
        await message.answer(text_help, reply_markup=markup)