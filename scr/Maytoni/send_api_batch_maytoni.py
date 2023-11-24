import requests
import json
import threading
from modules.Beauty_light3.scr.Maytoni import xml_to_dict_maytoni
from modules.Beauty_light3.logs import log_file_generator
import config
common_logger = log_file_generator.common_logger


def send_data_batch_stock(stocks_data, shop_name, warehouse_api_id):
    
    headers_oauth = config.headers

    base_url = f"https://api.partner.market.yandex.ru/campaigns/{warehouse_api_id}/offers/stocks"
    
    batch_size = 250
    for i in range(0, len(stocks_data), batch_size):
        batch = stocks_data[i:i+batch_size]

        response = requests.put(base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()
        
        if response.status_code == 200:
            print(f"Отправлен батч {i // batch_size + 1} Элементы до {i + batch_size}, магазин {shop_name}")
            pass
        else:
            print(f'Проблемы у {shop_name}', json.dumps(response_data, indent=2))
            

def main():
    stocks_data = xml_to_dict_maytoni.main()

    thread_stocks = threading.Thread(target=send_data_batch_stock, args=(stocks_data,
                                                                         "Maytoni",
                                                                         70946222))
    thread_stocks.start()

    thread_stocks.join()
