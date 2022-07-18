from get_floorplan_link import get_floorplan

import cv2
import requests
from pytesseract import pytesseract


def get_floorplan_text(rightmove_link: str):
    floorplan_link = get_floorplan(rightmove_link)

    if len(floorplan_link) == 0:
        return 0

    config = ('-l eng --oem 1 --psm 3')

    img_data = requests.get(floorplan_link[0]).content
    with open('tmp_data/floorplan.jpg', 'wb') as handler:
        handler.write(img_data)

    img = cv2.imread('tmp_data/floorplan.jpg')

    img = cv2.resize(img, (0, 0), fx=2, fy=2)

    img = cv2.convertScaleAbs(img, alpha=1.2, beta=-40)

    text = pytesseract.image_to_string(img, config=config)

    return text
