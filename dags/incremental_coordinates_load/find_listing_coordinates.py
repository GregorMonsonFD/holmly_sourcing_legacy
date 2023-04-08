from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
from scripts.python.get_all_coordinates_in_csv import get_all_coordinates
from airflow.utils.dates import days_ago
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(1),
    'yesterday': days_ago(2), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)

dag = DAG(
        dag_id='find_listing_coordinates',
        default_args=args,
        schedule_interval='0 0 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/coordinates'],
    )

with dag:
    area_task_sensor = ExternalTaskSensor(
        task_id='area_task_sensor',
        poke_interval=300,
        timeout=7200,
        soft_fail=False,
        retries=2,
        external_task_id='common_end_area',
        external_dag_id='find_listing_area',
        dag=dag
    )

    incremental_new_records_export = PostgresOperator(
        task_id='sql_incremental_load_coordinates_export',
        sql='incremental_new_records_export.sql',
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )


    sftp_download_from_db_coordinates = SFTPOperator(
        task_id="sftp_download_from_db_coordinates",
        ssh_conn_id="holmly_sftp",
        local_filepath="/home/eggzo/airflow/tmp_data/coordinates_export_{{ ds_nodash }}.csv",
        remote_filepath="/tmp/coordinates_export/coordinates_export_{{ ds_nodash }}.csv",
        operation="get",
        create_intermediate_dirs=True,
        retries=3,
    )

    find_all_coordinatess_incremental = PythonOperator(
        task_id='find_all_coordinates_incremental',
        provide_context=True,
        python_callable=get_all_coordinates,
        op_kwargs={'ds': '{{ ds_nodash }}', 'api_key': '{{ conn.googlemapsapi.password }}' },
        execution_timeout=datetime.timedelta(hours=16),
        retries=1,
    )

    sftp_upload_to_db_coordinates = SFTPOperator(
        task_id="sftp_upload_to_db_coordinates",
        ssh_conn_id="holmly_sftp",
        local_filepath="/home/eggzo/airflow/tmp_data/coordinates_export_{{ ds_nodash }}_filled.csv",
        remote_filepath="/tmp/coordinates_export_filled/coordinates_export_{{ ds_nodash }}_filled.csv",
        operation="put",
        create_intermediate_dirs=True,
        retries=3,
    )

    incremental_new_records_import = PostgresOperator(
        task_id='sql_incremental_load_coordinates_import',
        sql='incremental_new_records_import.sql',
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )

    common_end = DummyOperator(
        task_id='common_end_coordinates_load',
        dag=dag
    )

    area_task_sensor >> incremental_new_records_export
    incremental_new_records_export >> sftp_download_from_db_coordinates >> find_all_coordinatess_incremental
    find_all_coordinatess_incremental >> sftp_upload_to_db_coordinates >> incremental_new_records_import
    incremental_new_records_import >> common_end