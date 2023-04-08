from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from scripts.python.get_all_areas_in_csv import get_all_areas
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(1),
    'yesterday': days_ago(2), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)

dag = DAG(
        dag_id='find_listing_area',
        default_args=args,
        schedule_interval='0 0 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/floorplan'],# make this workflow happen every day
    )

with dag:
    rent_task_sensor = ExternalTaskSensor(
        task_id='rent_task_sensor',
        poke_interval=300,
        timeout=7200,
        soft_fail=False,
        retries=2,
        external_task_id='common_end_for_sale',
        external_dag_id='rightmove-scrape-for-sale',
        dag=dag
    )

    sale_task_sensor = ExternalTaskSensor(
        task_id='sale_task_sensor',
        poke_interval=300,
        timeout=7200,
        soft_fail=False,
        retries=2,
        external_task_id='task_to_be_sensed',
        external_dag_id='cloudwalker_dag_with_task_to_be_sensed',
        dag=dag
    )

    incremental_new_records_export = PostgresOperator(
        task_id='sql_incremental_load_floorplan_export',
        sql='incremental_new_records_export.sql',
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )


    sftp_download_from_db_floorplan = SFTPOperator(
        task_id="sftp_download_from_db_floorplan",
        ssh_conn_id="holmly_sftp",
        local_filepath="/home/eggzo/airflow/tmp_data/area_export_{{ ds_nodash }}.csv",
        remote_filepath="/tmp/area_export/area_export_{{ ds_nodash }}.csv",
        operation="get",
        create_intermediate_dirs=True,
        retries=3,
    )

    find_all_floorplans_incremental = PythonOperator(
        task_id='find_all_floorplans_incremental',
        provide_context=True,
        python_callable=get_all_areas,
        op_kwargs={'ds': '{{ ds_nodash }}'},
        execution_timeout=datetime.timedelta(hours=16),
        retries=1,
    )

    sftp_upload_to_db_floorplan = SFTPOperator(
        task_id="sftp_upload_to_db_floorplan",
        ssh_conn_id="holmly_sftp",
        local_filepath="/home/eggzo/airflow/tmp_data/area_export_{{ ds_nodash }}_filled.csv",
        remote_filepath="/tmp/area_export_filled/area_export_{{ ds_nodash }}_filled.csv",
        operation="put",
        create_intermediate_dirs=True,
        retries=3,
    )

    incremental_new_records_import = PostgresOperator(
        task_id='sql_incremental_load_floorplan_import',
        sql='incremental_new_records_import.sql',
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )

    common_end = DummyOperator(
        task_id='common_end_area_load',
        dag=dag
    )

    rent_task_sensor >> incremental_new_records_export
    sale_task_sensor >> incremental_new_records_export
    incremental_new_records_export >> sftp_download_from_db_floorplan >> find_all_floorplans_incremental
    find_all_floorplans_incremental >> sftp_upload_to_db_floorplan >> incremental_new_records_import
    incremental_new_records_import >> common_end

