import xml.etree.ElementTree as ET
import os
from datetime import datetime
from logs import log_file_generator

common_logger = log_file_generator.common_logger


def read_txt_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        my_list = [line.strip() for line in lines]
        return my_list
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None


def main():
    script_directory = os.path.dirname(__file__)
    download_folder = os.path.join(script_directory, '../../data/Stilfort/')
    file_path = os.path.join(download_folder, "Stilfort.xml")

    xml_file_path = file_path

    allow_folder = os.path.join(script_directory, '../../data/')
    file_path_allow = os.path.join(allow_folder, 'allow_list.txt')
    list_undebug_correct = read_txt_to_list(file_path_allow)

    stocks_data_stilfort = []

    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)

        root = tree.getroot()

        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')

        # Поиск всех элементов <offer>
        for offer_element in root.findall('.//offer'):

            article = offer_element.find('.//Артикул').text
            if article is None:
                continue

            article = article.replace(" ", "-").replace("+", "/")
            if article.lower() not in list_undebug_correct and article.upper() not in list_undebug_correct:
                continue

            article = article.lower()

            overleft = 0
            param_element = offer_element.find('.//param[@name="Остатки"]')
            value = param_element.text

            if value:
                if value == "более 10":
                    overleft = "11"
                else:
                    element_true = value.replace(" ", "").replace("шт", "")

                    if element_true is None:
                        overleft = "0"
                    elif int(element_true) <= 4:
                        overleft = "0"
                    else:
                        overleft = value

            stocks_data = {
                "sku": f"{article}",
                "warehouseId": 698807,
                "items": [
                    {
                        "count": overleft,
                        "type": "FIT",
                        "updatedAt": date_now,
                    }
                ]
            }

            stocks_data_stilfort.append(stocks_data)

        return stocks_data_stilfort

    except Exception as e:
        print(e)
        common_logger.info(f'Ошибка {e}')
        pass
