from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago



import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(0),
    'yesterday': days_ago(1), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)

dag = DAG(
        dag_id='find_listing_coordinates',
        default_args=args,
        schedule_interval='0 1 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/coordinates'],
    )

with dag:
    incremental_new_records_export = MySqlOperator(
        task_id='sql_incremental_load_coordinates_export',
        sql='incremental_new_records_export.sql',
        mysql_conn_id="mysql_warehouse",
        retries=3,
    )


    sftp_download_from_db_coordinates = SFTPOperator(
        task_id="sftp_download_from_db_coordinates",
        ssh_conn_id="sftp_default",
        local_filepath="/home/eggzo/airflow/tmp_data/coordinates_export_{{ ds_nodash }}.csv",
        remote_filepath="/var/lib/mysql-files/coordinates_export_{{ ds_nodash }}.csv",
        operation="get",
        create_intermediate_dirs=True,
        retries=3,
    )

    find_all_coordinatess_incremental = PythonOperator(
        task_id='find_all_coordinates_incremental',
        provide_context=True,
        python_callable=get_all_coordinatess,
        op_kwargs={'ds': '{{ ds_nodash }}'},
        execution_timeout=datetime.timedelta(hours=16),
        retries=1,
    )

    sftp_upload_to_db_coordinates = SFTPOperator(
        task_id="sftp_upload_to_db_coordinates",
        ssh_conn_id="sftp_default",
        local_filepath="/home/eggzo/airflow/tmp_data/coordinates_export_{{ ds_nodash }}_filled.csv",
        remote_filepath="/var/lib/mysql-files/coordinates_export_{{ ds_nodash }}_filled.csv",
        operation="put",
        create_intermediate_dirs=True,
        retries=3,
    )

    incremental_new_records_import = MySqlOperator(
        task_id='sql_incremental_load_coordinates_import',
        sql='incremental_new_records_import.sql',
        mysql_conn_id="mysql_warehouse",
        retries=3,
    )

    incremental_new_records_export >> sftp_download_from_db_coordinates >> find_all_coordinatess_incremental
    find_all_coordinatess_incremental >> sftp_upload_to_db_coordinates >> incremental_new_records_import