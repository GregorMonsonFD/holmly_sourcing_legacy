from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from scripts.python.pdfGen.report_generator import report_generator
from scripts.python.survey_monkey_distribute_daily import survey_monkey_distribute_daily
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

aws_command = "aws s3 cp /tmp/report_output/holmly_daily_report_{{ ds_nodash }}.pdf " + f"s3://sps-daily-reports/daily_reports/holmly_daily_report_{ datetime.datetime.today().strftime('%Y%m%d') }.pdf"

with dag:
    location_reporting_tables_task_sensor = ExternalTaskSensor(
        task_id='location_reporting_tables_task_sensor',
        poke_interval=300,
        timeout=7200,
        soft_fail=False,
        retries=2,
        external_task_id='common_end_location_reporting_tables',
        external_dag_id='location_reporting',
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

    sftp_upload_to_db_report = SFTPOperator(
        task_id="sftp_upload_to_db_report",
        ssh_conn_id="holmly_sftp",
        local_filepath="/home/eggzo/airflow/tmp_data/holmly_daily_report_{{ ds_nodash }}.pdf",
        remote_filepath="/tmp/report_output/holmly_daily_report_{{ ds_nodash }}.pdf",
        operation="put",
        create_intermediate_dirs=True,
        retries=3,
    )

    upload_report_to_s3 = SSHOperator(
        task_id="upload_report_to_s3",
        ssh_conn_id='holmly_ssh',
        command=aws_command,
    )

    common_end = DummyOperator(
        task_id='common_end_report_generation',
    )

    location_reporting_tables_task_sensor >> report_content_export
    report_content_export >> sftp_download_from_db_report_content >> generate_report
    generate_report >> sftp_upload_to_db_report >> upload_report_to_s3 >> common_end