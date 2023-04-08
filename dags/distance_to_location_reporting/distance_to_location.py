from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
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
    schedule_interval='0 0 * * *', # make this workflow happen every day
    template_searchpath=['/home/eggzo/airflow/scripts/sql/distance_to_location'],
)

with dag:
    locations = config.get('locations')

    coordinates_task_sensor = ExternalTaskSensor(
        task_id='coordinates_task_sensor',
        poke_interval=300,
        timeout=7200,
        soft_fail=False,
        retries=2,
        external_task_id='common_end_coordinates_load',
        external_dag_id='find_listing_coordinates',
        dag=dag
    )

    create_union_table = PostgresOperator(
        task_id='all_locations_reporting',
        sql='union_table.sql',
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )

    rental_reporting = PostgresOperator(
        task_id='all_rental_reporting',
        sql='rental_profitability.sql',
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )

    common_end = DummyOperator(
        task_id='common_end_location_reporting_tables',
        dag=dag
    )

    coordinates_task_sensor >> create_union_table

    for location in locations:

        if not location.get("is_active"):
            continue

        location_name = location["location_name"].replace(" ", "_")
        lat = location["lat"]
        long = location["long"]
        distance_km = location["distance"]

        reporting_task = report_sql(location_name, lat, long, distance_km)

        create_union_table >> reporting_task >> rental_reporting >> common_end
