import os
import sys
from scr.Stilfort import download_xml_Stilfort
from scr.Stilfort import send_api_batch_Stilfort
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


def main():
    download_xml_Stilfort.main()
    send_api_batch_Stilfort.main()


if __name__ == "__main__":
    main()
