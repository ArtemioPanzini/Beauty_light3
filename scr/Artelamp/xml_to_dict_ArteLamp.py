import xml.etree.ElementTree as ET
import os
from datetime import datetime
from modules.Beauty_light3.logs import log_file_generator
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
    download_folder = os.path.join(script_directory, '../../data/')
    file_path = os.path.join(download_folder, 'Artelamp.xml')
    xml_file_path = file_path

    allow_folder = os.path.join(script_directory, '../../data/')
    file_path_allow = os.path.join(allow_folder, 'allow_list.txt')
    list_undebug_correct = read_txt_to_list(file_path_allow)

    stocks_data_arte_lamp = []

    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)

        root = tree.getroot()

        # Создание списка для хранения отдельных <offer> элементов
        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')

        # Поиск всех элементов <offer>
        for offer_element in root.findall('.//offer'):

            article = offer_element.find('.//vendorCode').text
            article = article.replace(" ", "-").replace(',', '-')
            if article not in list_undebug_correct:
                continue

            overleft = 0
            outlet_element = offer_element.find('.//stock').text

            if outlet_element is not None:
                try:
                    overleft = round(float(outlet_element))
                    if overleft in (1, 2, 3, 4):
                        overleft = 0
                except Exception as e:
                    common_logger.info(f'Ошибка {e} во время разбора {article}')
                    pass

            stocks_data = {
                "sku": f"{article}",
                "warehouseId": 790859,
                "items": [
                    {
                        "count": overleft,
                        "type": "FIT",
                        "updatedAt": date_now,
                    }
                ]
            }

            stocks_data_arte_lamp.append(stocks_data)
        return stocks_data_arte_lamp

    except Exception as e:
        common_logger.info(f'Ошибка {e}')
        pass
