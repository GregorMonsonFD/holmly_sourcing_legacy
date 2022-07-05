from airflow.models import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
from scripts.python.rightmove_scrape import get_for_sale_properties
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(0),
    'yesterday': days_ago(1), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)

dag = DAG(
        dag_id='find_listing_area',
        default_args=args,
        schedule_interval='0 0 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/floorplan'],# make this workflow happen every day
    )

with dag:
    incremental_new_records_export = MySqlOperator(
        task_id='sql_incremental_load_floorplan_export',
        sql='incremental_new_records_export.sql',
        mysql_conn_id="mysql_warehouse",
        retries=3,
    )

    sftp_download_from_db = SFTPOperator(
        task_id="sftp_warehouse_to_pi",
        ssh_conn_id="sftp_default",
        local_filepath="/home/eggzo/airflow/tmp_data/area_export_{{ ds_nodash }}.csv",
        remote_filepath="/var/lib/mysql-files/area_export_{{ ds_nodash }}.csv",
        operation="get",
        create_intermediate_dirs=True,
        retries=3,
    )

    find_all_floorplans_incremental = PythonOperator(
        task_id='find_all_floorplans_incremental',
        provide_context=True,
        python_callable=get_for_sale_properties,
        execution_timeout=datetime.timedelta(seconds=600),
        retries=2,
    )

    sftp_upload_to_db = SFTPOperator(
        task_id="sftp_warehouse_to_pi",
        ssh_conn_id="sftp_default",
        local_filepath="/home/eggzo/airflow/tmp_data/area_export_{{ ds_nodash }}_filled.csv",
        remote_filepath="/var/lib/mysql-files/area_export_{{ ds_nodash }}_filled.csv",
        operation="put",
        create_intermediate_dirs=True,
        retries=3,
    )

    incremental_new_records_import = MySqlOperator(
        task_id='sql_incremental_load_floorplan_import',
        sql='incremental_new_records_export.sql',
        mysql_conn_id="mysql_warehouse",
        retries=3,
    )

    incremental_new_records_export >> sftp_download_from_db >> find_all_floorplans_incremental
    find_all_floorplans_incremental >> sftp_upload_to_db >> incremental_new_records_import