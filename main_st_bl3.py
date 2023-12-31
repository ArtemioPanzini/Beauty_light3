import sys
import time
import asyncio
import telegram
from datetime import datetime
from datetime import time as time_now
import config

import modules.Beauty_light3.scr.Artelamp.Artelamp_main as ArtelampMain
import modules.Beauty_light3.scr.Lightstar.Lightstar_main as LightstarMain
import modules.Beauty_light3.scr.Sonex.Sonex_main as SonexMain
import modules.Beauty_light3.scr.Favourite.favourite_main as FavouriteMain
import modules.Beauty_light3.scr.Maytoni.Maytoni_main as MaytoniMain
import modules.Beauty_light3.scr.Stilfort.Stilfort_main as StilfortMain


sys.path.append('\\home\\scrapping\\Beauty_light\\')


class MessageHandler:
    def __init__(self):
        self.bot_token = config.telegram_api_token  # Укажите ваш токен Telegram бота
        self.bot = telegram.Bot(token=self.bot_token)
        self.list_default_for_telegram = ['Maytoni', 'LightStar', 'Sonex', 'Stilfort', 'ArteLamp', 'Favourite']
        self.list_success_for_telegram = []

        self.user_data = {
            'Рома': {'user_name': 'Рома', 'user_id': 328128719},
            'Арен': {'user_name': 'Аваг', 'user_id': 1454597584},
            'Артем': {'user_name': 'Артем', 'user_id': 312956486}
        }

    async def make_message_for_tg(self, some_list, user='Артем'):
        user_data = self.user_data.get(user, self.user_data['Артем'])

        dict_for_tg = {}
        if len(some_list) == 5:
            dict_for_tg[user_data['user_id']] = f'Остатки {user} - всё окей'
            dict_for_tg[user_data['user_id']] = 'Сегодня все остатки обновлены'
            return dict_for_tg

        elif len(some_list) < 5:
            for item in self.list_success_for_telegram:
                if item in self.list_default_for_telegram:
                    self.list_default_for_telegram.remove(item)
            dict_for_tg[user_data['user_id']] = f'Не отправились {user_data["user_name"]} ' \
                                                f'{", ".join(self.list_default_for_telegram)}'

            dict_for_tg[user_data['user_id']] = f'Остатки обновились в {", ".join(some_list)} и не обновились в ' \
                                                f'{", ".join(self.list_default_for_telegram)}'
            return dict_for_tg

        elif len(some_list) > 5:
            dict_for_tg[user_data['Артем']] = f'Обнаружен лишний магазин у {user_data["user_name"]}'
            # отправлять какой именно
            return dict_for_tg

        else:
            dict_for_tg[user_data['Артем']] = f'Что-то не так'
            return dict_for_tg

    async def add_to_success_list(self, item):
        self.list_success_for_telegram.append(item)


async def send_messages_to_users(message_dict):
    message_handler = MessageHandler()
    for user_id, message in message_dict.items():
        try:
            await message_handler.bot.send_message(chat_id=user_id, text=message)
            print(f"Сообщение отправлено пользователю с ID {user_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю с ID {user_id}: {e}")


async def main():
    message_handler = MessageHandler()
    start_api_time = time.time()

    try:
        print('ArteLampApiMain BL3 start')
        ArtelampMain.main()
        await message_handler.add_to_success_list('ArteLamp')
        print(f'ArteLampApiMain BL3 success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(f'В ScrappingMain BL3 ошибка: {e}')
        time.sleep(60)

    try:
        print('FavouriteMain BL3 start')
        FavouriteMain.main()
        await message_handler.add_to_success_list('Favourite')
        print(f'Favourite success BL3 ждём 58с')
        time.sleep(58)
    except Exception as e:
        print(f'В FavouriteMain BL3 ошибка: {e}')
        time.sleep(118)

    try:
        print('MaytoniMain BL3 start')
        MaytoniMain.main()
        await message_handler.add_to_success_list('Maytoni')
        print(f'Maytoni success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(f'В MaytoniMain BL3 ошибка: {e}')
        time.sleep(120)

    try:
        print('LightstarMain BL3 start')
        LightstarMain.main()
        await message_handler.add_to_success_list('LightStar')
        print(f'LightStar success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(f'В LightStar BL3 ошибка: {e}')
        time.sleep(120)

    try:
        print('StilfortMain BL3 start')
        StilfortMain.main()
        await message_handler.add_to_success_list('Stilfort')
        print(f'StilfortApiMain success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(e)
        print(f'В StilfortMain BL3 ошибка: {e}')
        time.sleep(120)

    try:
        print('SonexMain BL3 start')
        SonexMain.main()
        await message_handler.add_to_success_list('Sonex')
        print(f"SonexMain success, ничего не ждём")
    except Exception as e:
        print(f'В SonexMain BL3 ошибка: {e}')

    time_interval1_start = time_now(9, 45)
    time_interval1_end = time_now(10, 00)
    current_time = datetime.now().time()

    # Проверяем, находится ли текущее время в интервале 9:45 - 10:00
    if time_interval1_start <= current_time <= time_interval1_end:
        message_dict = await message_handler.make_message_for_tg(message_handler.list_success_for_telegram, 'Арен')

        await send_messages_to_users(message_dict)
    else:
        pass

    end_api_time = time.time()
    execution_api_time = end_api_time - start_api_time
    print(f"Время выполнения по Api: {execution_api_time} секунд")


if __name__ == '__main__':
    asyncio.run(main())
