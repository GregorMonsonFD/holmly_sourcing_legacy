# from get_all_areas_in_csv import get_all_areas

import re
import pandas as pd

from extract_text import get_floorplan_text

def get_all_areas(ds):
    regex_ft = '[\d\,\.]+(?=\s*(?:sq|square)(?:\.\s*|\s*)f)'
    regex_m = '[\d\,\.]+(?=\s*(?:sq|square)(?:\.\s*|\s*)m)'

    sq_m_to_ft_factor = 10.7639

    input_df = pd.read_csv(f"/home/eggzo/airflow/tmp_data/area_export_{ ds }.csv", header=None)
    output_df = pd.DataFrame()

    for index, row in input_df.iterrows():
        sq_ft_total = 0
        text = get_floorplan_text(row[1])

        print(text)

        if text == 0:
            output_df.append([row[0], row[1], 0, 'null', 'null'], ignore_index=True)
            continue

        sq_ft = re.findall(regex_ft, text[0])
        sq_m = re.findall(regex_m, text[0])

        print(sq_ft, sq_m)

        if len(sq_ft) != 0:
            for i in range(len(sq_ft)):
                sq_ft[i] = sq_ft[i].replace(',', '')

            for area in sq_ft:
                sq_ft_total = sq_ft_total + float(area)

            for area in sq_ft:
                if float(area) >= (sq_ft_total/2)*0.95 and float(area) <= (sq_ft_total/2)*1.05:
                    sq_ft_total = max(sq_ft)

            output_df.append([row[0], row[1], text[1], sq_ft_total, text[0]], ignore_index=True)
        elif len(sq_m) != 0:
            for i in range(len(sq_m)):
                sq_m[i] = sq_m[i].replace(',', '')

            for area in sq_m:
                sq_ft_total = sq_ft_total + float(area)

            for area in sq_ft:
                if float(area) >= (sq_ft_total/2)*0.95 and float(area) <= (sq_ft_total/2)*1.05:
                    sq_ft_total = max(sq_ft)

            sq_ft_total = sq_ft_total * sq_m_to_ft_factor


            output_df.append([row[0], row[1], text[1], sq_ft_total, text[0]], ignore_index=True)

        elif len(sq_m) == 0 and len(sq_ft) == 0:

            output_df.append([row[0], row[1], text[1], 'null', text[0]], ignore_index=True)

    print(output_df)
    output_df.to_csv(f"/home/eggzo/airflow/tmp_data/area_export_{ ds }_filled.csv", header=None)
