from modules.Beauty_light3.scr.Maytoni import download_xml_maytoni
from modules.Beauty_light3.scr.Maytoni import send_api_batch_maytoni


def main():
    download_xml_maytoni.main()
    send_api_batch_maytoni.main()


if __name__ == "__main__":
    main()
