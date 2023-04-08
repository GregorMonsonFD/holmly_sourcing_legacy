from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
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
        schedule_interval='0 0 * * *',
        template_searchpath=['/home/eggzo/airflow/scripts/sql/report_content'],# make this workflow happen every day
    )

with dag:
    location_reporting_tables_task_sensor = ExternalTaskSensor(
        task_id='location_reporting_tables_task_sensor',
        poke_interval=300,
        timeout=7200,
        soft_fail=False,
        retries=2,
        external_task_id='location_reporting',
        external_dag_id='find_listing_coordinates',
        dag=dag
    )

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
        task_id='generate_daily_report',
        provide_context=True,
        python_callable=report_generator,
        op_kwargs={'ds': '{{ ds_nodash }}'},
        execution_timeout=datetime.timedelta(hours=1),
        retries=1,
    )

    location_reporting_tables_task_sensor >> report_content_export
    report_content_export >> sftp_download_from_db_report_content >> generate_report