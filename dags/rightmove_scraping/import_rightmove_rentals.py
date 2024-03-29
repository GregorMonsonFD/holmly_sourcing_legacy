from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from scripts.python.rightmove_scrape_rental import get_to_rent_properties
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(1),
    'yesterday': days_ago(2), # make start date in the past
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

globals()[f'rightmove-scrape-to-rent'] = DAG(
        dag_id=f'rightmove-scrape-to-rent',
        default_args=args,
        schedule_interval='0 0 * * *', # make this workflow happen every day
        template_searchpath=['/home/eggzo/airflow/scripts/sql/db_operations_rental'],
    )

common_end = DummyOperator(
    task_id='common_end_to_rent',
    dag=globals()['rightmove-scrape-to-rent']
    )

for region in config.get('imports'):

    if not region.get("is_active"):
        continue

    rightmove_region = region["rightmove_region"]
    region_name = region["region_name"]
    postcode_prefix = region["postcode_prefix"]
    ds = '{{ ds }}'

    with globals()[f'rightmove-scrape-to-rent']:

        rightmove_to_csv = PythonOperator(
            task_id=f'rightmove_{ region_name }_to_csv',
            provide_context=True,
            python_callable=get_to_rent_properties,
            execution_timeout=datetime.timedelta(seconds=1200),
            op_kwargs={'borough': rightmove_region},
            params={'rightmove_region': rightmove_region},
            retries=2,
        )

        sftp_upload_to_db = SFTPOperator(
            task_id=f"sftp_{ region_name }_pi_to_warehouse",
            ssh_conn_id="holmly_sftp",
            local_filepath="/home/eggzo/airflow/tmp_data/rental_data_{{ params.rightmove_region }}_{{ ds }}.csv",
            remote_filepath="/tmp/rightmove_scrape/rental_data_{{ params.rightmove_region }}_{{ ds }}.csv",
            operation="put",
            create_intermediate_dirs=True,
            params={'rightmove_region': rightmove_region},
            retries=3,
        )

        delete_csv_local = BashOperator(
            task_id=f'delete_{ region_name }_csv_local',
            bash_command=f'rm /home/eggzo/airflow/tmp_data/rental_data_{ rightmove_region }_{ ds }.csv'
        )

        sql_insert_ids = postgresql_group(SQL_files[2], rightmove_region, region_name, postcode_prefix)

        staging_to_refined = postgresql_group(SQL_files[6], rightmove_region, region_name, postcode_prefix)

        rightmove_to_csv >> sftp_upload_to_db

        sftp_upload_to_db >> postgresql_group(SQL_files[0], rightmove_region, region_name, postcode_prefix) >> postgresql_group(SQL_files[1], rightmove_region, region_name, postcode_prefix) >> sql_insert_ids

        for i in range(3, 6):
            sql_insert_ids >> postgresql_group(SQL_files[i], rightmove_region, region_name, postcode_prefix) >> staging_to_refined
        
        staging_to_refined >> delete_csv_local >> common_end
