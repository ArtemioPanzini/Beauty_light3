#!/bin/bash
export PATH=/home/scrapping/Beauty_light/venv/bin:$PATH
export VIRTUAL_ENV=/home/scrapping/Beauty_light
# Путь к активации виртуальной среды
path_to_activate="/home/scrapping/Beauty_light/venv/bin/activate"

# Активировать виртуальную среду
source "$path_to_activate"
echo "all good"
# Путь к вашему основному скрипту
path_to_script="/home/scrapping/Beauty_light/main_stock.py"

# Запустить ваш основной скрипт
python3 "$path_to_script"
