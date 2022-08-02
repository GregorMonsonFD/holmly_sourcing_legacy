# from get_all_areas_in_csv import get_all_areas

import googlemaps
import pandas as pd

def get_all_coordinates(**kwargs):
    ds_nodash = kwargs['ds']
    input_df = pd.read_csv(f"/home/eggzo/airflow/tmp_data/coordinates_export_{ ds_nodash }.csv", header=None)
    output_df = pd.DataFrame(columns=['id', 'longitude', 'latitude'])

    gmaps = googlemaps.Client(key=kwargs['api_key'])

    for index, row in input_df.iterrows():

        geocode_result = gmaps.geocode(row[1])
        print(geocode_result)

        lng = geocode_result[0]['geometry']['location']['lng']
        lat = geocode_result[0]['geometry']['location']['lat']

        tmp_data = [row[0], lng, lat]
        print(tmp_data)

        output_df.loc[len(output_df)] = tmp_data

    print(output_df)
    output_df.to_csv(f"/home/eggzo/airflow/tmp_data/coordinates_export_{ ds_nodash }_filled.csv", header=None, index=False)
