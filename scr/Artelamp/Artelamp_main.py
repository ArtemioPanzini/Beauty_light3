from modules.Beauty_light3.scr.Artelamp import download_xml_ArteLamp
from modules.Beauty_light3.scr.Artelamp import send_api_batch_ArteLamp


def main():
    download_xml_ArteLamp.main()
    send_api_batch_ArteLamp.main()


if __name__ == "__main__":
    main()
