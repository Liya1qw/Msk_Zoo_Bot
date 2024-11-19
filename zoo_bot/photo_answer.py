from aiogram import types
from questins_answers import list_animal
from description_animal import description
from urllib.parse import quote

class PhotoAnswer:
    @staticmethod
    async def photo_res(message: types.Message, chosen_animal):
        text = ('Поздравляю с прохождением викторины! 🎉\n\n'
                f'Твое тотемное животное - {chosen_animal} 😍\n')
        site = "<a href='https://moscowzoo.ru/'>Московского зоопарка</a>"
        friend_club = ('Ты можешь взять это животное под опеку!\n'
                       f'Участие в программе «Клуб друзей зоопарка» — это помощь в содержании обитателей {site}, а также твой личный вклад в дело сохранения биоразнообразия Земли и развитие зоопарка :)\n'
                       'Тыкай по кнопке "Клуб друзей", чтобы узнать больше о программе опеки ❤️')

        encoded_text = quote(text)
        clean_text = encoded_text.replace('%20', ' ')
        vk_share_url = f'https://vk.com/share.php?url=https://t.me/Msk_Zoo_quiz_bot&title={clean_text}&description={clean_text}'

        markup = types.InlineKeyboardMarkup(row_width=1)
        restart_quiz = types.InlineKeyboardButton('Попробовать еще раз?', callback_data='quiz')
        btn_review = types.InlineKeyboardButton('Написать отзыв', callback_data='review')
        btn_friend = types.InlineKeyboardButton('Круг друзей 🫰🏻', url='https://moscowzoo.ru/about/guardianship')
        btn_share_vk = types.InlineKeyboardButton('Поделиться в ВКонтакте', url=vk_share_url)
        btn_back = types.InlineKeyboardButton('Назад в начало', callback_data='start')
        markup.add(restart_quiz, btn_review, btn_friend, btn_share_vk, btn_back)
        for index, animal in enumerate(list_animal, start=1):
            if animal == chosen_animal:
                animal_desc = description[index-1]
                full_text = f'{text}\n{animal_desc}\n\n{friend_club}'

                photo_path = f'photo/photo_{index}.jpg'
                with open(photo_path, 'rb') as file:
                    print('Вывод результата')
                    await message.answer_photo(file, full_text, parse_mode="HTML", reply_markup=markup)
                break

