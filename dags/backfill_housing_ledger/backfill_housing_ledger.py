from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from scripts.python.rightmove_scrape import get_for_sale_properties
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
}

LOCAL_PATH = os.path.dirname(__file__)
config_file = os.path.join(LOCAL_PATH, "imports.yml")

with open(config_file, "r") as infile:
    config = yaml.full_load(infile)


def postgresql_group(name, rightmove_region, region_name, postcode_prefix, **kwargs):
    return PostgresOperator(
        task_id='sql_{}_{}'.format(name[:-4], region_name),
        sql=name,
        params={
            'rightmove_region': rightmove_region,
            'region_name': region_name,
            'postcode_prefix': postcode_prefix
        },
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )

SQL_files = (
        [
            'create_tables.sql',
            'csv_to_landing_area.sql',
            'insert_ids.sql',
            'price_conversion.sql',
            'updating_static_fields.sql',
            'address_extraction.sql',
            'staging_to_refined.sql'
        ]
        )

dag = DAG(
        dag_id=f'backfill_housing_ledger',
        start_date=datetime.datetime(2022, 9, 1),
        catchup=True,
        default_args=args,
        schedule_interval='0 12 * * *', # make this workflow happen every day
        template_searchpath=['/home/eggzo/airflow/scripts/sql/db_operations'],
    )

for region in config.get('imports'):

    if not region.get("is_active"):
        continue

    rightmove_region = region["rightmove_region"]
    region_name = region["region_name"]
    postcode_prefix = region["postcode_prefix"]
    ds = '{{ ds }}'

    sql_insert_ids = postgresql_group(SQL_files[2], rightmove_region, region_name, postcode_prefix)

    staging_to_refined = postgresql_group(SQL_files[6], rightmove_region, region_name, postcode_prefix)

    postgresql_group(SQL_files[0], rightmove_region, region_name, postcode_prefix) >> postgresql_group(SQL_files[1], rightmove_region, region_name, postcode_prefix) >> sql_insert_ids
