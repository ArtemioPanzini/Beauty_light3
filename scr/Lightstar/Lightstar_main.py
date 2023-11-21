import os
import sys
from scr.Lightstar import download_xml_lightstar
from scr.Lightstar import send_api_batch_lightstar

#  Добавляем корневую папку main для path append
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')) )


def main():
    download_xml_lightstar.main()
    send_api_batch_lightstar.main()


if __name__ == "__main__":
    main()
