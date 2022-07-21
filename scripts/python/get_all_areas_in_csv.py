# from get_all_areas_in_csv import get_all_areas

import re
import pandas as pd

from extract_area import get_floorplan_text

def get_all_areas(ds):
    regex_ft = '\d+(?=\s*(?:sq|square)(?:\.\s*|\s*)f)'
    regex_m = '\d+(?=\s*(?:sq|square)(?:\.\s*|\s*)m)'

    df = pd.read_csv(f"/home/eggzo/airflow/tmp_data/area_export_{ ds }.csv", header=None)

    #x = re.findall(regex_ft, placeholder_text)
    #y = re.findall(regex_m, placeholder_text)


    #print(x, y)
    print(df)
