# from get_all_areas_in_csv import get_all_areas

import re
from geopy.geocoders import Nominatim
import pandas as pd

from scripts.python.extract_text import get_floorplan_text

def get_all_coordinates(**kwargs):
    ds_nodash = kwargs['ds']
    input_df = pd.read_csv(f"/home/eggzo/airflow/tmp_data/coordinates_export_{ ds_nodash }.csv", header=None)
    output_df = pd.DataFrame(columns=['id', 'longitude', 'latitude'])

    geolocator = Nominatim(user_agent="gm_finding_for_sale_house_coordinates")

    for index, row in input_df.iterrows():

        location = geolocator.geocode(row[1])

        tmp_data = [row[0], location.longitude, location.latitude]
        print(tmp_data)

        output_df.loc[len(output_df)] = tmp_data

    print(output_df)
    output_df.to_csv(f"/home/eggzo/airflow/tmp_data/coordinates_export_{ ds_nodash }_filled.csv", header=None, index=False)
