import xml.etree.ElementTree as ET
import os
from datetime import datetime
from datetime import time
from datetime import date

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
    download_folder = os.path.join(script_directory, '../../data/Maytoni/')
    file_path = os.path.join(download_folder, 'Maytoni.yml')
    xml_file_path = file_path

    allow_folder = os.path.join(script_directory, '../../data/')
    file_path_allow = os.path.join(allow_folder, 'allow_list.txt')
    list_undebug_correct = read_txt_to_list(file_path_allow)

    stocks_data = []
    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')

        for offer_element in root.findall('.//offer'):

            if offer_element.find('vendor').text == 'Voltega':
                continue

            article = offer_element.get('id')
            if article is None:
                continue
            if article not in list_undebug_correct:
                continue

            overleft = 0

            try:
                outlet_element = offer_element.find('.//outlet')
                overleft_wo_round = outlet_element.get('instock')
                if overleft_wo_round == "-1":
                    overleft = 0
                overleft = round(float(overleft_wo_round))
                if overleft == 1 or overleft == 2 or overleft == 3 or overleft == 4:
                    overleft = 0
            except Exception as e:
                common_logger.info(f'Ошибка {e} во время разбора {article}')

            if overleft < 0:
                overleft = 0

            stock_data = {
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

            stocks_data.append(stock_data)
        return stocks_data
    except Exception as e:
        common_logger.info(f'Ошибка {e}')
        pass


# Пример использования функции
if __name__ == '__main__':
    main()
