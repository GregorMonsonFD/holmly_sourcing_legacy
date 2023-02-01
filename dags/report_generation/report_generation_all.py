from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from scripts.python.pdfGen.report_generator import report_generator
import datetime, os, yaml

args = {
    'owner': 'Gregor Monson',
    'start_date': days_ago(1),
    'yesterday': days_ago(2), # make start date in the past
}

LOCAL_PATH = os.path.dirname(__file__)

dag = DAG(
        dag_id='report_generate_daily',
        default_args=args,
        schedule_interval='0 10 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/report_content'],# make this workflow happen every day
    )

with dag:
    report_content_export = PostgresOperator(
        task_id='sql_report_content_export',
        sql='report_content_export.sql',
        postgres_conn_id="holmly-postgresql",
        retries=3,
    )


    sftp_download_from_db_report_content = SFTPOperator(
        task_id="sftp_download_from_db_report_content",
        ssh_conn_id="holmly_sftp",
        local_filepath="/home/eggzo/airflow/tmp_data/report_content_{{ ds_nodash }}.csv",
        remote_filepath="/tmp/report_content/report_content_{{ ds_nodash }}.csv",
        operation="get",
        create_intermediate_dirs=True,
        retries=3,
    )

    generate_report = PythonOperator(
        task_id='find_all_floorplans_incremental',
        provide_context=True,
        python_callable=report_generator,
        op_kwargs={'ds': '{{ ds_nodash }}'},
        execution_timeout=datetime.timedelta(hours=1),
        retries=1,
    )

    report_content_export >> sftp_download_from_db_report_content >> generate_report