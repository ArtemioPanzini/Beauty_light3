import os
import sys
from scr.Maytoni import download_xml_maytoni
from scr.Maytoni import send_api_batch_maytoni
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


def main():
    download_xml_maytoni.main()
    send_api_batch_maytoni.main()


if __name__ == "__main__":
    main()
