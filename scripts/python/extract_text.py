from get_floorplan_link import get_floorplan

import cv2
import requests
from pytesseract import pytesseract


def get_floorplan_text(rightmove_link: str):
    floorplan_link = get_floorplan(rightmove_link)

    try:
        if len(floorplan_link) == 0:
            return 0

        config = ('-l eng --oem 1 --psm 3')

        img_data = requests.get(floorplan_link[0]).content
        with open('/home/eggzo/airflow/tmp_data/floorplan.jpg', 'wb') as handler:
            handler.write(img_data)

        img = cv2.imread('/home/eggzo/airflow/tmp_data/floorplan.jpg')

        img = cv2.resize(img, (0, 0), fx=2, fy=2)

        img = cv2.convertScaleAbs(img, alpha=1.2, beta=-40)

        text = str(pytesseract.image_to_string(img, config=config))

        return [text, len(floorplan_link)]

    except:
        return 0
