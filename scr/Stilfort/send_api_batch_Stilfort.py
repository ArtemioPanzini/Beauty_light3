import requests
import json
import threading
import time
from modules.Beauty_light3.scr.Stilfort import xml_to_dict_Stilfort
from modules.Beauty_light3.logs import log_file_generator
import config
common_logger = log_file_generator.common_logger


def send_data_batch_stock(stocks_data, shop_name, warehouse_api_id):
    headers_oauth = config.headers

    base_url = f"https://api.partner.market.yandex.ru/campaigns/{warehouse_api_id}/offers/stocks"

    # Переменные для управления отправкой запросов
    batch_size = 250
    max_requests_per_minute = 5000

    requests_sent_in_minute = 0
    # Разбиваем prices_data на батчи размером 250
    batches = [stocks_data[i:i + batch_size] for i in range(0, len(stocks_data), batch_size)]

    for batch in batches:
        if requests_sent_in_minute >= max_requests_per_minute:
            print("Достигнут лимит запросов. Ожидание...")
            time.sleep(60)  # Подождать 1 минуту
            requests_sent_in_minute = 0  # Сбросить счетчик

        response = requests.put(base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()

        requests_sent_in_minute += len(batch)  # Увеличить счетчик запросов

        if response.status_code == 200:
            print(f"Остатки {shop_name}: Отправлен батч с {requests_sent_in_minute} элементами")
            pass
        else:
            print(json.dumps(response_data, indent=2))


def main():
    stocks_data_stilfort = xml_to_dict_Stilfort.main()
    print(f'Остатки Stilfort: {len(stocks_data_stilfort)}')
    thread_stocks_stilfort = threading.Thread(target=send_data_batch_stock, args=(stocks_data_stilfort, "Stilfort",
                                                                                  70946222))
    thread_stocks_stilfort.start()

    thread_stocks_stilfort.join()
