import xml.etree.ElementTree as ET
import requests
import time as timeless
import json
import threading
import os
from datetime import datetime


def read_txt_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        my_list = [line.strip() for line in lines]
        return my_list
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None


def send_data_batch_stock(stocks_data, headers_oauth):
    base_url = "https://api.partner.market.yandex.ru/campaigns/62747703/offers/stocks"

    batch_size = 500
    for i in range(0, len(stocks_data), batch_size):
        batch = stocks_data[i:i + batch_size]

        response = requests.put(base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()

        if response.status_code == 200:
            pass
        else:
            print(json.dumps(response_data, indent=2))


def main():
    start_time = datetime.now()

    date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')
    url = "https://ftp.favourite-light.com/ForClients/export/offers.xml"

    response = requests.get(url)
    timeless.sleep(1)

    # Создаем список для хранения данных о ценах
    stocks_data = []

    script_directory = os.path.dirname(__file__)
    allow_folder = os.path.join(script_directory, '../../data/')
    file_path_allow = os.path.join(allow_folder, 'allow_list.txt')
    list_undebug_incorrect = read_txt_to_list(file_path_allow)

    # Проверка на успешное получение файла
    if response.status_code == 200:
        # Разбор XML-данных
        xml_data = response.content
        root = ET.fromstring(xml_data)

        # Итерация по элементам <item>
        for item in root.findall(".//Номенклатура"):
            article = item.get("Имя")
            article = article.replace(" ", "-")
            if article not in list_undebug_incorrect:
                continue

            stock = item.find("Остаток").text if item.find("Остаток") is not None else None
            if stock == '1' or stock == '-1' or stock == '2' or stock == '3' or stock == '4':
                stock = 0
            elif stock == 'более 10':
                stock = 11
            elif stock == 'более 50':
                stock = 51
            else:
                stock = stock

            stock_data = {
                "sku": f"{article}",
                "warehouseId": 698807,
                "items": [
                    {
                        "count": stock,
                        "type": "FIT",
                        "updatedAt": date_now,
                    }
                ]
            }
            stocks_data.append(stock_data)

    # Отображаем общее количество элементов для отправки
    headers_oauth = {"Authorization": "Bearer y0_AgAAAABW45BlAApomAAAAADrXWqYcge3WjPZQj2l-zlBmGYZGZAehy0"}
    thread_stocks = threading.Thread(target=send_data_batch_stock, args=(stocks_data, headers_oauth))

    thread_stocks.start()

    # Ожидание завершения потоков
    thread_stocks.join()

    end_time = datetime.now()

    finally_time = end_time - start_time
    print(f"Favourite {finally_time}")


if __name__ == "__main__":
    main()
