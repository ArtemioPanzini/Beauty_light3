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
    download_folder = os.path.join(script_directory, '../../data/LightStar/')
    file_path = os.path.join(download_folder, 'LightStar.yml')
    xml_file_path = file_path

    allow_folder = os.path.join(script_directory, '../../data/')
    file_path_allow = os.path.join(allow_folder, 'allow_list.txt')
    list_undebug_correct = read_txt_to_list(file_path_allow)

    stocks_data_lightstar = []
    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Создание списка для хранения отдельных <offer> элементов
        offers = {}
        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')

        # Поиск всех элементов <offer>
        for offer_element in root.findall('.//offer'):

            article = offer_element.find('.//vendorCode').text
            if article not in list_undebug_correct:
                continue

            overleft = 0

            try:
                outlet_element = offer_element.find('.//stock').text
                if outlet_element:
                    overleft = round(float(outlet_element))
                else:
                    overleft = 0

                if overleft in (1, 2, 3, 4):
                    overleft = 0
            except Exception as e:
                common_logger.info(f'Ошибка {e} во время разбора {article}')

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

            stocks_data_lightstar.append(stocks_data)
        return stocks_data_lightstar

    except Exception as e:
        common_logger.info(f'Ошибка {e}')
        pass


if __name__ == "__main__":
    main()
