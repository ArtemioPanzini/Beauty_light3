import requests
import json
import threading
from scr.Lightstar import xml_to_dict_lightstar
from logs import log_file_generator

common_logger = log_file_generator.common_logger


def send_data_batch_stock(stocks_data, shop_name, warehouse_api_id):
    
    headers_oauth = {"Authorization": "Bearer y0_AgAAAABW45BlAApomAAAAADrXWqYcge3WjPZQj2l-zlBmGYZGZAehy0"}

    base_url = f"https://api.partner.market.yandex.ru/campaigns/{warehouse_api_id}/offers/stocks"
    
    batch_size = 250
    for i in range(0, len(stocks_data), batch_size):
        batch = stocks_data[i:i+batch_size]

        response = requests.put(base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()
        
        if response.status_code == 200:
            print(f"Отправлены остатки {i // batch_size + 1} Элементы до {i + batch_size}, магазин {shop_name}")
            pass
        else:
            print(f'Проблемы у {shop_name}',json.dumps(response_data, indent=2))
            

def main():
    stocks_data_lightstar = xml_to_dict_lightstar.main()

    thread_stocks_lightstar = threading.Thread(target=send_data_batch_stock, args=(stocks_data_lightstar, "lightstar",
                                                                                   62747703))
    thread_stocks_lightstar.start()
    thread_stocks_lightstar.join()
