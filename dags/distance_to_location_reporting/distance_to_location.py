from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
import os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(1),
    'yesterday': days_ago(2), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)
config_file = os.path.join(LOCAL_PATH, "locations_of_interest.yml")

with open(config_file, "r") as infile:
    config = yaml.full_load(infile)


def report_sql(location_name, lat, long, distance_km):
    return PostgresOperator(
        task_id='{}_reporting'.format(location_name),
        sql='distance_scoring.sql',
        params={
            'location': location_name,
            'lat': lat,
            'long': long,
            'distance': distance_km
        },
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )

dag = DAG(
    dag_id='location_reporting',
    default_args=args,
    schedule_interval='0 8 * * *', # make this workflow happen every day
    template_searchpath=['/home/eggzo/airflow/scripts/sql/distance_to_location'],
)

with dag:

    for location in config.get('locations'):

        if not location.get("is_active"):
            continue

        location_name = location["location_name"].replace(" ", "_")
        lat = location["lat"]
        long = location["long"]
        distance_km = location["distance"]

        report_sql(location_name, lat, long, distance_km)
