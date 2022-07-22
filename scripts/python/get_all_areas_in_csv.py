# from get_all_areas_in_csv import get_all_areas

import re
import pandas as pd

from scripts.python.extract_text import get_floorplan_text


def clean_up_text(set: list):
    for i in range(len(set)):
        set[i] = set[i].replace(',', '')

        if set[i] == '.':
            set.pop(i)
            continue

        set[i] = float(set[i])

    return set


def get_all_areas(**kwargs):
    ds_nodash = kwargs['ds']
    regex_ft = '[\d\,\.]+(?=\s*(?:sq|square)(?:\.\s*|\s*)f)'
    regex_m = '[\d\,\.]+(?=\s*(?:sq|square)(?:\.\s*|\s*)m)'

    sq_m_to_ft_factor: float = 10.7639

    input_df = pd.read_csv(f"/home/eggzo/airflow/tmp_data/area_export_{ ds_nodash }.csv", header=None)
    output_df = pd.DataFrame(columns=['id', 'link', 'number_of_floorplans', 'area', 'text'])

    for index, row in input_df.iterrows():
        sq_ft_total = 0.0
        text = get_floorplan_text(row[1])

        print(text)

        if text == 0:
            tmp_data = [row[0], row[1], 0, 'null', 'null']
            output_df.loc[len(output_df)] = tmp_data
            continue

        sq_ft = re.findall(regex_ft, text[0])
        sq_m = re.findall(regex_m, text[0])

        sq_ft = clean_up_text(sq_ft)
        sq_m = clean_up_text(sq_m)

        print(sq_ft, sq_m)

        if len(sq_ft) != 0:

            for area in sq_ft:
                sq_ft_total = sq_ft_total + area

            sq_ft_max = max(sq_ft)

            if sq_ft_max >= (sq_ft_total / 2) * 0.95 and area <= (sq_ft_total / 2) * 1.05:
                sq_ft_total = max(sq_ft)

            tmp_data = [row[0], row[1], text[1], sq_ft_total, text[0]]
            output_df.loc[len(output_df)] = tmp_data

        elif len(sq_m) != 0:

            for i in range(len(sq_m)):
                sq_m[i] = sq_m[i] * sq_m_to_ft_factor
                sq_ft_total = sq_ft_total + area

            sq_ft_max = max(sq_m)

            if sq_ft_max >= (sq_ft_total / 2) * 0.95 and area <= (sq_ft_total / 2) * 1.05:
                sq_ft_total = max(sq_m)

            sq_ft_total = sq_ft_total * sq_m_to_ft_factor

            tmp_data = [row[0], row[1], text[1], sq_ft_total, text[0]]
            output_df.loc[len(output_df)] = tmp_data

        elif len(sq_m) == 0 and len(sq_ft) == 0:
            tmp_data = [row[0], row[1], text[1], 'null', text[0]]
            output_df.loc[len(output_df)] = tmp_data

    print(output_df)
    output_df.to_csv(f"/home/eggzo/airflow/tmp_data/area_export_{ ds_nodash }_filled.csv", header=None, index=False)
