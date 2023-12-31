import requests
import os
from modules.Beauty_light3.logs import log_file_generator
common_logger = log_file_generator.common_logger


def delete_file_if_exist(source_path):
    if os.path.isfile(source_path):
        os.remove(source_path)
        common_logger.info(f'Файл удален: {source_path}')


def download_file(file_url, target_path):
    response = requests.get(file_url)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, 'wb') as file:
            file.write(response.content)
            
        common_logger.info(f'Файл скачан и сохранен в {target_path}')
    else:
        common_logger.error(f'Не удалось скачать файл. Код статуса: {response.status_code}')


def main():
    # URL файла для загрузки
    file_url = 'https://lightstar.ru/image/yml/lightstar_rozn_dolgop_stock.yml'

    # Полный путь к текущему скрипту
    script_directory = os.path.dirname(__file__)

    # Папка для сохранения загруженных файлов
    download_folder = os.path.join(script_directory, '../../data/LightStar/')
    
    # Имя файла из URL
    file_name = os.path.basename("LightStar.yml")

    # Полный путь к файлу для сохранения
    file_path = os.path.join(download_folder, file_name)

    delete_file_if_exist(file_path)
    download_file(file_url, file_path)


if __name__ == '__main__':
    main()
